document.getElementById('btn-verify').addEventListener('click', async () => {
    const text = quill.getText().trim();
    const outputDiv = document.getElementById('verification-result');
    const contentDiv = outputDiv.querySelector('.result-content');

    if (!text) {
        alert("Veuillez saisir du texte d'abord.");
        return;
    }

    try {
        contentDiv.textContent = "Vérification en cours...";
        outputDiv.style.display = 'block';

        const response = await fetch('/api/correct', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        
        // Affichage du résultat corrigé ou des erreurs trouvées
        // On suppose que l'API renvoie un champ 'correctedText' ou 'errors'
        const resultText = data.correctedText ? "Texte corrigé :\n" + data.correctedText : JSON.stringify(data, null, 2);
        contentDiv.textContent = resultText;
        
    } catch (err) {
        console.error("Erreur vérification :", err);
        contentDiv.textContent = "Erreur lors de la vérification.";
    }
});