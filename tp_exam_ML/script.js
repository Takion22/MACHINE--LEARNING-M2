// Avec Quill.js comme éditeur rich text
const quill = new Quill('#editor', { theme: 'snow' });

quill.on('text-change', async () => {
    const text = quill.getText().trim();
    const words = text.split(/\s+/).filter(Boolean);
    
    // On prend les 2 derniers mots comme contexte
    const context = words.slice(-2);
    
    if (context.length === 0) return;
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ context })
        });
        
        const { suggestions } = await response.json();
        displaySuggestions(suggestions);
        
    } catch (err) {
        console.error("Erreur prédiction :", err);
    }
});

function displaySuggestions(words) {
    const box = document.getElementById('suggestions');
    box.innerHTML = '';
    
    words.forEach(word => {
        const btn = document.createElement('button');
        btn.textContent = word;
        
        // Clic sur une suggestion : l'insérer dans l'éditeur
        btn.onclick = () => {
            const pos = quill.getLength() - 1;
            quill.insertText(pos, ' ' + word);
            box.innerHTML = ''; // cacher les suggestions
        };
        
        box.appendChild(btn);
    });
}