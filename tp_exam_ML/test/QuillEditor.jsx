import React, { useEffect, useRef, useState } from 'react';
import Quill from 'quill';
import { getPredictions } from './api';

const QuillEditor = ({ onSuggestionsUpdate, onStatusChange, onContextChange }) => {
  const editorRef = useRef(null);
  const quillInstance = useRef(null);
  const overlayRef = useRef(null);
  const [currentSuggestion, setCurrentSuggestion] = useState(null);
  
  // Initialisation de Quill
  useEffect(() => {
    if (!editorRef.current) return;

    quillInstance.current = new Quill(editorRef.current, {
      theme: 'snow',
      placeholder: 'Tapez votre texte en malgache... (Tab pour accepter)',
      modules: {
        toolbar: [
          ['bold', 'italic', 'underline'],
          ['blockquote', 'code-block'],
          [{ 'list': 'ordered'}, { 'list': 'bullet' }]
        ]
      }
    });

    // Gestionnaire de changement de texte
    let debounceTimer;
    
    quillInstance.current.on('text-change', () => {
      clearTimeout(debounceTimer);
      
      const text = quillInstance.current.getText().trim();
      const words = text.split(/\s+/).filter(Boolean);
      const context = words.slice(-2);
      
      onContextChange(context);

      if (context.length === 0) {
        clearSuggestions();
        return;
      }

      // Debounce API call
      debounceTimer = setTimeout(async () => {
        try {
          onStatusChange('loading', '🔄 Chargement...');
          const data = await getPredictions(context);
          const suggestions = data.suggestions || [];
          
          onSuggestionsUpdate(suggestions);
          
          if (suggestions.length > 0) {
            setCurrentSuggestion(suggestions[0]);
            updateOverlayPosition();
          } else {
            clearSuggestions();
          }
          
          onStatusChange('', '');
        } catch (err) {
          onStatusChange('error', '❌ Erreur de prédiction');
          clearSuggestions();
        }
      }, 300);
    });

    // Mise à jour position overlay au clic/déplacement
    quillInstance.current.on('selection-change', (range) => {
      if (range && currentSuggestion) {
        updateOverlayPosition();
      }
    });

  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Run once on mount

  // Effet pour gérer l'affichage de l'overlay quand la suggestion change
  useEffect(() => {
    if (currentSuggestion) {
      updateOverlayPosition();
    }
  }, [currentSuggestion]);

  const updateOverlayPosition = () => {
    try {
      const selection = quillInstance.current.getSelection();
      if (!selection || !overlayRef.current) return;
      
      const bounds = quillInstance.current.getBounds(selection.index);
      if (bounds) {
        overlayRef.current.style.top = bounds.top + 'px';
        overlayRef.current.style.left = bounds.left + 'px';
        overlayRef.current.style.display = 'block';
      }
    } catch (e) {
      console.log('Position update error:', e);
    }
  };

  const clearSuggestions = () => {
    setCurrentSuggestion(null);
    onSuggestionsUpdate([]);
    if (overlayRef.current) overlayRef.current.style.display = 'none';
  };

  const insertSuggestion = (word) => {
    const selection = quillInstance.current.getSelection();
    if (selection) {
      quillInstance.current.insertText(selection.index, word + ' ');
      quillInstance.current.setSelection(selection.index + word.length + 1);
      clearSuggestions();
    }
  };

  // Exposer la méthode d'insertion au parent via un event listener personnalisé ou une ref
  // Pour simplifier ici, on écoute les changements de props ou on utilise useImperativeHandle
  // Mais pour React, on va attacher la fonction au window temporairement ou passer une ref
  // Solution propre : Gestionnaire d'événements clavier
  
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!currentSuggestion) return;
      
      // Tab ou Ctrl+Right
      if ((e.key === 'Tab' || (e.ctrlKey && e.key === 'ArrowRight'))) {
        e.preventDefault();
        insertSuggestion(currentSuggestion);
      }
      // Esc
      else if (e.key === 'Escape') {
        clearSuggestions();
      }
    };

    // On attache l'écouteur au div de l'éditeur pour ne pas capturer tous les événements de la page
    const editorDiv = document.querySelector('.ql-editor');
    if(editorDiv) editorDiv.addEventListener('keydown', handleKeyDown);
    
    return () => {
        if(editorDiv) editorDiv.removeEventListener('keydown', handleKeyDown);
    };
  }, [currentSuggestion]);

  return (
    <div className="editor-wrapper">
      <div ref={editorRef} id="editor-container"></div>
      <div ref={overlayRef} className="suggestion-overlay">
        {currentSuggestion}
      </div>
    </div>
  );
};

export default QuillEditor;