from lissage import predict_with_interpolation, vocab
from modele_n_grams import model_1, model_2, model_3

# Test de l'autocomplétion
context = ["trano"]  # Exemple de contexte
models = {1: model_1, 2: model_2, 3: model_3}
suggestions = predict_with_interpolation(context, models, vocab, top_k=1)
print("Suggestions pour le contexte", context, ":", suggestions)