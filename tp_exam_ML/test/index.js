import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // StrictMode est désactivé temporairement car il provoque un double rendu 
  // qui peut interférer avec l'initialisation de Quill v1.3
  // <React.StrictMode>
    <App />
  // </React.StrictMode>
);