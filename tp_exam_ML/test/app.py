import os
import sys
from pathlib import Path

# Ajouter le dossier parent à PYTHONPATH pour que les modules puissent être importés.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, render_template, request, jsonify
from lissage import predict_with_interpolation, vocab
from modele_n_grams import model_1, model_2, model_3
from flask_cors import CORS

app = Flask(__name__, template_folder='.', static_folder='.')

# Activer CORS pour permettre les requêtes depuis React (localhost:3000)
CORS(app)

# Préparer les modèles
models = {1: model_1, 2: model_2, 3: model_3}

@app.route('/')
def index():
    """Servir la page principale"""
    return render_template('index_inline.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API pour obtenir les suggestions d'autocomplétion"""
    try:
        data = request.get_json()
        context = data.get('context', [])
        top_k = data.get('top_k', 5)
        
        if not context or len(context) == 0:
            return jsonify({'suggestions': []})
        
        # Appeler la fonction d'interpolation avec cache
        suggestions = predict_with_interpolation(
            context, 
            models, 
            vocab, 
            top_k=top_k
        )
        
        return jsonify({'suggestions': suggestions})
    
    except Exception as e:
        print(f"Erreur API: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de santé"""
    return jsonify({'status': 'ok', 'corpus_size': len(vocab)})

if __name__ == '__main__':
    print(f"Serveur démarré avec {len(vocab)} mots dans le vocabulaire")
    app.run(debug=True, port=5000, host='127.0.0.1')
