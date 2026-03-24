from collections import Counter
from tokenisations import tokens    
import math

# Cache pour les prédictions fréquentes
prediction_cache = {}

def predict_with_laplace(model, vocab, context, alpha=1, top_k=5):
    """
    Ajoute 'alpha' à chaque comptage pour éviter les probabilités nulles.
    Utile pour les contextes rares mais existants.
    """
    counts = model.get(tuple(context), Counter())
    
    # Probabilité lissée pour chaque mot du vocabulaire
    total = sum(counts.values()) + alpha * len(vocab)
    scores = {
        word: (counts.get(word, 0) + alpha) / total
        for word in vocab
    }
    
    # Retourner les top_k meilleurs scores
    sorted_words = sorted(scores, key=scores.get, reverse=True)
    return sorted_words[:top_k]

def predict_with_interpolation(context, models, vocab, lambdas=[0.5, 0.3, 0.2], alpha=1, top_k=5):
    """
    Interpolation linéaire des modèles avec lissage de Laplace.
    Utilise des probabilités logarithmiques pour éviter les underflows numériques.
    lambdas : poids pour [unigram, bigram, trigram]
    Utilise un cache pour les prédictions fréquentes.
    """
    ctx_key = tuple(context)
    if ctx_key in prediction_cache:
        return prediction_cache[ctx_key]
    
    scores = {}
    for word in vocab:
        score = 0.0
        for i, model in enumerate([models[1], models[2], models[3]], 1):
            ctx = context[- (i-1):] if len(context) >= i-1 else context
            counts = model.get(tuple(ctx), Counter())
            total = sum(counts.values()) + alpha * len(vocab)
            prob = (counts.get(word, 0) + alpha) / total
            if prob > 0:
                score += lambdas[i-1] * math.log(prob)
        scores[word] = score
    
    # Retourner les top_k meilleurs scores (plus élevé = meilleure probabilité)
    sorted_words = sorted(scores, key=scores.get, reverse=True)[:top_k]
    prediction_cache[ctx_key] = sorted_words
    return sorted_words

vocab = set(tokens)  # tous les mots uniques du corpus