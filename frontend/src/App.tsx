import React, { useState } from 'react';
import './App.css';
import VoiceInterface from './components/VoiceInterface';
import AdminPanel from './components/AdminPanel';

function App() {
  const [currentView, setCurrentView] = useState<'main' | 'admin'>('main');

  // Vérifier si l'URL contient /admin
  React.useEffect(() => {
    if (window.location.pathname.includes('/admin')) {
      setCurrentView('admin');
    }
  }, []);

  if (currentView === 'admin') {
    return <AdminPanel />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔍 Agence Hackosint - Mission Golf</h1>
        <p>Enquête en cours - Contact Brigade Criminelle Marseille requis</p>
        <button 
          className="admin-link" 
          onClick={() => setCurrentView('admin')}
          title="Accès administration (personnel autorisé uniquement)"
        >
          🔒
        </button>
      </header>
      <main>
        <VoiceInterface />
      </main>
      <footer className="App-footer">
        <p className="disclaimer">
          ⚠️ Cette enquête est fictive - Réalisée dans le cadre du CTF organisé par Hackolyte
        </p>
      </footer>
    </div>
  );
}

export default App;
