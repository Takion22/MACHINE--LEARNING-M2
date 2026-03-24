document.getElementById('btn-lemmatize').addEventListener('click', async () => {
    const text = quill.getText().trim();
    const outputDiv = document.getElementById('lemmatisation-result');
    const contentDiv = outputDiv.querySelector('.result-content');

    if (!text) {
        alert("Veuillez saisir du texte d'abord.");
        return;
    }

    try {
        contentDiv.textContent = "Analyse en cours...";
        outputDiv.style.display = 'block';

        const response = await fetch('/api/lemmatize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        // On suppose que l'API renvoie le texte lemmatisé ou une liste de lemmes
        contentDiv.textContent = JSON.stringify(data, null, 2);
        
    } catch (err) {
        console.error("Erreur lemmatisation :", err);
        contentDiv.textContent = "Erreur lors de la lemmatisation.";
    }
});