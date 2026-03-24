import React, { useState } from 'react';
import './App.css';
import QuillEditor from './components/QuillEditor';

function App() {
  const [suggestions, setSuggestions] = useState([]);
  const [context, setContext] = useState([]);
  const [status, setStatus] = useState({ type: '', msg: '' });

  const handleStatusChange = (type, msg) => {
    setStatus({ type, msg });
  };

  const handleInsertFromButton = (word) => {
    // Cette logique nécessite une communication vers l'enfant (QuillEditor)
    // Pour faire simple dans cette migration, on simule l'appui TAB
    // Dans une app React parfaite, on utiliserait un Context ou un Store
    // Ici, on va utiliser un événement custom dispatché sur l'éditeur
    const editor = document.querySelector('.ql-editor');
    if (editor) {
        editor.focus();
        // Insertion manuelle via l'instance Quill serait plus propre si on avait levé l'état de Quill
        // Mais pour l'instant, disons à l'utilisateur d'utiliser le clavier ou on implémente plus tard
        alert(`Cliquez dans l'éditeur et appuyez sur Tab pour insérer "${word}" (L'insertion au clic bouton nécessite une refactorisation plus poussée)`);
    }
  };

  return (
    <div className="container">
      <h1>✨ Autocomplétion Malagasy</h1>
      <p className="subtitle">Version React - Écrivez en malgache avec IA</p>
      
      <div className="editor-section">
        <label>Éditeur de texte</label>
        
        <QuillEditor 
          onSuggestionsUpdate={setSuggestions}
          onStatusChange={handleStatusChange}
          onContextChange={setContext}
        />

        <div className="context-display">
          <strong>Contexte courant :</strong> <span>{context.length > 0 ? JSON.stringify(context) : '-'}</span>
        </div>
        
        <div className={`status ${status.type}`}>
          {status.msg}
        </div>

        <div className="keyboard-shortcuts">
          <p><strong>⌨️ Raccourcis clavier :</strong></p>
          <p>• <strong>Tab</strong> ou <strong>Ctrl+→</strong> : Accepter la suggestion</p>
          <p>• <strong>Esc</strong> : Rejeter la suggestion</p>
        </div>
      </div>
      
      <div className="suggestions-section">
        <span className="suggestions-label">💡 Autres suggestions</span>
        <div className={`suggestions-list ${suggestions.length === 0 ? 'empty' : ''}`}>
          {suggestions.length === 0 ? (
            'Commencez à taper...'
          ) : (
            suggestions.map((word, idx) => (
              <button key={idx} className="suggestion-btn" onClick={() => handleInsertFromButton(word)}>
                {word} {idx === 0 ? '⭐' : ''}
              </button>
            ))
          )}
        </div>
      </div>
      
      <div className="footer">
        Made with ❤️ | ML Autocompletion System - React Architecture
      </div>
    </div>
  );
}

export default App;