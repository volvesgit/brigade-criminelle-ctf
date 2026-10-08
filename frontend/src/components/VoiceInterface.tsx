import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Phone, PhoneCall, PhoneOff, Mic, MicOff, MessageSquare, Trophy } from 'lucide-react';
import axios from 'axios';
import './VoiceInterface.css';

interface ChatMessage {
  type: 'user' | 'claire';
  content: string;
  timestamp: Date;
}

interface APIResponse {
  response: string;
  audio_base64?: string;
  flag_found: boolean;
}

const VoiceInterface: React.FC = () => {
  const [isCallActive, setIsCallActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [flagFound, setFlagFound] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const [sessionId, setSessionId] = useState<string>('');
  
  const audioRef = useRef<HTMLAudioElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  // Configuration de l'API backend
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://backend-production-0c4b.up.railway.app';

  // Fonction pour générer un nouvel ID de session
  const generateSessionId = () => {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  };  const playAudio = useCallback((audioBase64: string) => {
    try {
      console.log('Attempting to play audio, base64 length:', audioBase64.length);
      
      // Décoder le base64 en bytes
      const binaryString = atob(audioBase64);
      const bytes = new Uint8Array(binaryString.length);
      for (let i = 0; i < binaryString.length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
      }
      
      // Créer le blob avec les bytes décodés - OpenAI TTS retourne du MP3
      const audioBlob = new Blob([bytes], { type: 'audio/mp3' });
      const audioUrl = URL.createObjectURL(audioBlob);
      
      console.log('Audio blob created, size:', audioBlob.size, 'type: audio/mp3');
      
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        
        // Configurer l'élément audio
        audioRef.current.preload = 'auto';
        audioRef.current.controls = false;
        
        // Gérer les événements pour debug
        audioRef.current.onloadstart = () => console.log('Audio loading started');
        audioRef.current.oncanplay = () => console.log('Audio can play');
        audioRef.current.onplay = () => console.log('Audio started playing');
        audioRef.current.onended = () => {
          console.log('Audio playback ended');
          URL.revokeObjectURL(audioUrl);
        };
        audioRef.current.onerror = (e) => {
          console.error('Audio error:', e);
          console.error('Audio error details:', audioRef.current?.error);
        };
        
        // Jouer l'audio
        const playPromise = audioRef.current.play();
        if (playPromise !== undefined) {
          playPromise
            .then(() => {
              console.log('Audio playback successful');
            })
            .catch(error => {
              console.error('Audio playback failed:', error);
              // Essayer de jouer après interaction utilisateur
              if (error.name === 'NotAllowedError') {
                console.log('Audio blocked by browser, user interaction required');
                // Créer un bouton pour permettre à l'utilisateur de déclencher l'audio
                alert('Cliquez sur OK pour permettre la lecture audio');
                audioRef.current?.play().catch(e => console.error('Second attempt failed:', e));
              }
            });
        }
      }
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  }, []);
  // Fonction pour terminer l'appel
  const endCall = useCallback(async () => {
    try {
      await axios.post(`${API_BASE_URL}/api/end-call`);
      setIsCallActive(false);
      setMessages([]);
      setFlagFound(false);
      setSessionId(''); // Réinitialiser l'ID de session pour chaque nouvel appel
    } catch (error) {
      console.error('Erreur lors de la fin de l\'appel:', error);
    }
  }, [API_BASE_URL]);

  const handleSendMessage = useCallback(async (message: string) => {
    if (!message.trim() || isLoading) return;

    // Ajouter le message utilisateur
    const userMessage: ChatMessage = {
      type: 'user',
      content: message,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);    try {
      const response = await axios.post<APIResponse>(`${API_BASE_URL}/api/chat`, {
        message: message,
        session_id: sessionId
      });// Ajouter la réponse de l'Inspecteur
      const claireMessage: ChatMessage = {
        type: 'claire',
        content: response.data.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, claireMessage]);      // Vérifier si le flag a été trouvé
      if (response.data.flag_found) {
        setFlagFound(true);
        
        // Auto-terminer l'appel après un délai plus court pour permettre d'entendre le message
        setTimeout(() => {
          console.log('🎯 FLAG TROUVÉ - Mission terminée - Fin automatique de l\'appel');
          endCall();
        }, 5000); // 5 secondes pour permettre d'entendre le message complet
      }

      // Jouer l'audio de la réponse
      if (response.data.audio_base64) {
        console.log('Received audio data, attempting to play...');
        playAudio(response.data.audio_base64);
      }

    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);      const errorMessage: ChatMessage = {
        type: 'claire',
        content: 'Désolé, j\'ai des problèmes de ligne. Pouvez-vous répéter ?',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);    } finally {
      setIsLoading(false);
    }
  }, [API_BASE_URL, isLoading, playAudio, sessionId, endCall]);
  // Initialisation de la reconnaissance vocale
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = true;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'fr-FR';
        recognitionInstance.onresult = (event) => {
        let finalTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        
        if (finalTranscript && isCallActive) {
          handleSendMessage(finalTranscript);
          setIsRecording(false);
        }
      };
      
      recognitionInstance.onerror = (event) => {
        console.error('Erreur de reconnaissance vocale:', event.error);
        setIsRecording(false);
      };
      
      recognitionInstance.onend = () => {
        setIsRecording(false);
      };
      
      setRecognition(recognitionInstance);
    }
  }, [isCallActive, handleSendMessage]);

  // Auto-scroll vers le bas des messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);  const startCall = async () => {
    try {
      setIsLoading(true);
      
      // Générer un nouvel ID de session pour chaque appel
      const newSessionId = generateSessionId();
      setSessionId(newSessionId);
      
      const response = await axios.post(`${API_BASE_URL}/api/start-call`);
      
      setIsCallActive(true);
      setMessages([{
        type: 'claire',
        content: response.data.greeting,
        timestamp: new Date()
      }]);
      
      // Jouer l'audio d'accueil si disponible
      if (response.data.audio_base64) {
        console.log('Playing welcome audio...');
        playAudio(response.data.audio_base64);
      }
      
    } catch (error) {
      console.error('Erreur lors du démarrage de l\'appel:', error);
      alert('Impossible de démarrer l\'appel. Vérifiez que le serveur backend est lancé.');
    } finally {
      setIsLoading(false);
    }
  };

  // Fonction de test pour l'audio
  const testAudio = async () => {
    try {
      console.log('Testing audio functionality...');
      const response = await axios.post(`${API_BASE_URL}/api/chat`, {
        message: "test audio",
        session_id: sessionId || "test_session"
      });
      
      if (response.data.audio_base64) {
        console.log('Test audio received, playing...');
        playAudio(response.data.audio_base64);
      } else {
        console.log('No audio data received');
      }
    } catch (error) {
      console.error('Error testing audio:', error);
    }
  };  const startRecording = () => {
    if (recognition && !isRecording && isCallActive) {
      setIsRecording(true);
      recognition.start();
    }
  };

  const stopRecording = () => {
    if (recognition && isRecording) {
      recognition.stop();
      setIsRecording(false);
    }
  };

  // Gestion des événements de souris et tactiles pour maintenir le bouton
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    startRecording();
  };

  const handleMouseUp = (e: React.MouseEvent) => {
    e.preventDefault();
    stopRecording();
  };

  const handleMouseLeave = (e: React.MouseEvent) => {
    e.preventDefault();
    if (isRecording) {
      stopRecording();
    }
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    e.preventDefault();
    startRecording();
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    e.preventDefault();
    stopRecording();
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(inputText);
    }
  };

  return (
    <div className="voice-interface">      {flagFound && (
        <div className="flag-success">
          <Trophy size={48} />
          <h2>🎉 MISSION TERMINÉE AVEC SUCCÈS !</h2>
          <p>FLAG TROUVÉ : Jules Lefèvre</p>
          <p>L'appel va se terminer automatiquement...</p>
        </div>
      )}

      <div className="phone-container">        <div className="phone-header">
          <Phone className="phone-icon" />
          <h2>Brigade Criminelle - Inspecteur Dubois</h2>
          <div className={`status-indicator ${isCallActive ? 'active' : 'inactive'}`}>
            {isCallActive ? '🟢 En ligne' : '🔴 Hors ligne'}
          </div>
        </div>        {!isCallActive ? (
          <div className="call-start">            <button 
              className="start-call-btn"
              onClick={startCall}
              disabled={isLoading}
            >
              <PhoneCall size={24} />
              {isLoading ? 'Connexion...' : 'Contacter Brigade Criminelle'}
            </button>
              <button 
              className="test-audio-btn"
              onClick={testAudio}
              disabled={isLoading}
              style={{
                marginTop: '10px',
                padding: '8px 16px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              🔊 Test Audio
            </button>
            
            <div className="roleplay-hints">
              <h3>🎭 Conseils Roleplay</h3>
              <ul>
                <li><strong>🎯 Incarnez votre rôle :</strong> Vous êtes un enquêteur de l'agence Hackosint</li>
                <li><strong>💬 Parlez naturellement :</strong> Utilisez un langage professionnel mais conversationnel</li>
                <li><strong>🕵️ Soyez crédible :</strong> Présentez-vous, donnez un contexte à votre appel</li>
                <li><strong>📝 Écoutez attentivement :</strong> Le Brigadier vous donnera des indices précieux</li>
                <li><strong>🎪 Jouez le jeu :</strong> Réagissez aux informations, posez des questions de suivi</li>
                <li><strong>⏰ Patience :</strong> Laissez la conversation se développer naturellement</li>
              </ul>            </div>
          </div>
        ) : (
          <div className="call-interface">
            <div className="messages-container">              {messages.map((message, index) => (
                <div key={index} className={`message ${message.type}`}>
                  <div className="message-content">
                    <strong>{message.type === 'user' ? 'Enquêteur Hackosint' : 'Brigadier'}:</strong>
                    <p>{message.content}</p>
                  </div>
                  <span className="message-time">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                </div>
              ))}              {isLoading && (
                <div className="message ai loading">
                  <div className="message-content">
                    <strong>Inspecteur Dubois:</strong>
                    <p>...</p>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="input-container">
              <div className="text-input-section">
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Tapez votre message ici..."
                  disabled={isLoading}
                  rows={2}
                />
                <button
                  onClick={() => handleSendMessage(inputText)}
                  disabled={isLoading || !inputText.trim()}
                  className="send-btn"
                >
                  <MessageSquare size={20} />
                </button>
              </div>

              <div className="voice-controls">                <button
                  className={`voice-btn ${isRecording ? 'recording' : ''}`}
                  onMouseDown={handleMouseDown}
                  onMouseUp={handleMouseUp}
                  onMouseLeave={handleMouseLeave}
                  onTouchStart={handleTouchStart}
                  onTouchEnd={handleTouchEnd}
                  disabled={isLoading}
                >
                  {isRecording ? <MicOff size={24} /> : <Mic size={24} />}
                  {isRecording ? 'Relâchez pour arrêter' : 'Maintenir pour parler'}
                </button>
              </div>

              <button className="end-call-btn" onClick={endCall}>
                <PhoneOff size={20} />
                Raccrocher
              </button>
            </div>
          </div>
        )}      </div>

      <audio ref={audioRef} />
    </div>
  );
};

export default VoiceInterface;
