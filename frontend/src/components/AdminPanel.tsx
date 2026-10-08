import React, { useState, useEffect, useCallback } from 'react';
import './AdminPanel.css';

interface Conversation {
  id: string;
  timestamp: string;
  messages: Array<{
    type: 'user' | 'ai';
    content: string;
    timestamp: string;
  }>;
  flag_found: boolean;
  user_info?: {
    ip?: string;
    user_agent?: string;
  };
}

const AdminPanel: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [token, setToken] = useState<string>('');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [lastRefresh, setLastRefresh] = useState<Date | null>(null);  // Configuration de l'API backend
  const getApiBaseUrl = () => {
    // Si REACT_APP_API_URL est définie, l'utiliser
    if (process.env.REACT_APP_API_URL) {
      return process.env.REACT_APP_API_URL;
    }
      // Si nous sommes sur Railway (production), utiliser l'URL de production
    if (window.location.hostname.includes('railway.app')) {
      return 'https://backend-production-0c4b.up.railway.app';
    }
    
    // Sinon, utiliser localhost pour le développement
    return 'http://localhost:8080';
  };
  
  const API_BASE_URL = getApiBaseUrl();

  const fetchConversations = useCallback(async (authToken?: string) => {
    if (!isAuthenticated && !authToken) return;
    
    setLoading(true);
    const currentToken = authToken || token;
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/admin/conversations`, {
        headers: {
          'Authorization': `Bearer ${currentToken}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setConversations(data.conversations || []);
        setLastRefresh(new Date());
        console.log('Conversations loaded:', data); // Debug
      } else {
        setError('Erreur lors du chargement des conversations');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated, token, API_BASE_URL]);

  // Actualisation automatique toutes les secondes
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isAuthenticated && autoRefresh) {
      // Charger les données immédiatement
      fetchConversations();
      
      // Puis actualiser toutes les secondes
      interval = setInterval(() => {
        fetchConversations();
      }, 1000);
    }
      return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isAuthenticated, autoRefresh, fetchConversations]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
      try {
      const response = await fetch(`${API_BASE_URL}/api/admin/auth`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password }),
      });

      const data = await response.json();
      
      if (response.ok && data.authenticated) {
        setIsAuthenticated(true);
        setToken(data.token);
        setError('');
        fetchConversations(data.token);
      } else {
        setError('Mot de passe incorrect');
        setPassword('');
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
      setPassword('');    } finally {
      setLoading(false);
    }  };

  // Modifier le useEffect pour corriger les dépendances
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isAuthenticated && autoRefresh) {
      // Charger les données immédiatement
      fetchConversations();
      
      // Puis actualiser toutes les secondes
      interval = setInterval(() => {
        fetchConversations();
      }, 1000);
    }
    
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [isAuthenticated, autoRefresh, fetchConversations]);

  const refreshData = () => {
    fetchConversations();
  };

  if (!isAuthenticated) {
    return (
      <div className="admin-login">
        <div className="login-container">
          <h2>🔐 Administration - Brigade Criminelle</h2>
          <p>Accès restreint - Identification requise</p>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="password">Mot de passe d'accès :</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Entrez le mot de passe admin"
                required
              />
            </div>
            {error && <div className="error-message">{error}</div>}
            <button type="submit" className="login-btn">
              Accéder au panel
            </button>
          </form>
          <div className="security-notice">
            ⚠️ Accès autorisé uniquement au personnel de la Brigade Criminelle
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-panel">
      <header className="admin-header">
        <h1>🕵️ Panel d'Administration - Surveillance CTF</h1>
        <div className="header-info">
          {lastRefresh && (
            <span className="last-refresh">
              Dernière MAJ: {lastRefresh.toLocaleTimeString()}
            </span>
          )}
        </div>
        <div className="header-actions">
          <button 
            onClick={() => setAutoRefresh(!autoRefresh)} 
            className={`auto-refresh-btn ${autoRefresh ? 'active' : ''}`}
          >
            {autoRefresh ? '⏸️ Pause Auto' : '▶️ Auto Refresh'}
          </button>
          <button onClick={refreshData} className="refresh-btn">
            🔄 Actualiser
          </button>
          <button onClick={() => setIsAuthenticated(false)} className="logout-btn">
            🚪 Déconnexion
          </button>
        </div>
      </header>

      <div className="admin-content">
        <div className="sidebar">
          <h3>💬 Conversations ({conversations.length})</h3>
          {loading ? (
            <div className="loading">Chargement...</div>
          ) : (
            <div className="conversations-list">
              {conversations.map((conv) => (
                <div
                  key={conv.id}
                  className={`conversation-item ${selectedConversation === conv.id ? 'selected' : ''}`}
                  onClick={() => setSelectedConversation(conv.id)}
                >
                  <div className="conv-header">
                    <span className="conv-id">#{conv.id.substring(0, 8)}</span>
                    {conv.flag_found && <span className="flag-indicator">🏁 FLAG</span>}
                  </div>
                  <div className="conv-time">{new Date(conv.timestamp).toLocaleString()}</div>
                  <div className="conv-messages">{conv.messages.length} messages</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="main-content">
          {selectedConversation ? (
            <ConversationDetail 
              conversation={conversations.find(c => c.id === selectedConversation)} 
            />
          ) : (
            <div className="no-selection">
              <h3>Sélectionnez une conversation pour voir les détails</h3>
              <p>Panel de surveillance des interactions CTF</p>
              <div className="stats">
                <div className="stat-item">
                  <span className="stat-number">{conversations.length}</span>
                  <span className="stat-label">Total conversations</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{conversations.filter(c => c.flag_found).length}</span>
                  <span className="stat-label">Flags trouvés</span>
                </div>
                <div className="stat-item">
                  <span className="stat-number">{conversations.reduce((acc, c) => acc + c.messages.length, 0)}</span>
                  <span className="stat-label">Messages total</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const ConversationDetail: React.FC<{ conversation?: Conversation }> = ({ conversation }) => {
  if (!conversation) return null;

  return (
    <div className="conversation-detail">
      <div className="detail-header">
        <h3>Conversation #{conversation.id.substring(0, 8)}</h3>
        <div className="detail-info">
          <span>📅 {new Date(conversation.timestamp).toLocaleString()}</span>
          {conversation.flag_found && <span className="flag-found">🏁 FLAG TROUVÉ</span>}
        </div>
      </div>

      <div className="messages-container">
        {conversation.messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            <div className="message-header">
              <span className="sender">{message.type === 'user' ? '👤 Utilisateur' : '🤖 IA'}</span>
              <span className="time">{new Date(message.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="message-content">{message.content}</div>
          </div>
        ))}
      </div>

      {conversation.user_info && (
        <div className="user-info">
          <h4>ℹ️ Informations techniques</h4>
          <p><strong>IP:</strong> {conversation.user_info.ip || 'N/A'}</p>
          <p><strong>User Agent:</strong> {conversation.user_info.user_agent || 'N/A'}</p>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
