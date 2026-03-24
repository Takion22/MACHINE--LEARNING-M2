from nltk import ngrams
from collections import defaultdict, Counter
from tokenisations import tokens

def build_ngram_model(tokens, n=3):
    """
    Construit un dictionnaire : contexte → comptage des mots suivants
    Exemple pour n=3 (trigramme) :
      ("ny", "vary") → Counter({"masaka": 45, "mena": 12, "fotsy": 8})
    """
    model = defaultdict(Counter)
    
    for gram in ngrams(tokens, n):
        context = gram[:-1]    # les N-1 premiers mots
        next_word = gram[-1]   # le dernier mot (celui à prédire)
        model[context][next_word] += 1
    
    return model

# On construit plusieurs modèles pour le backoff
model_3 = build_ngram_model(tokens, n=3)  # trigrammes
model_2 = build_ngram_model(tokens, n=2)  # bigrammes
model_1 = build_ngram_model(tokens, n=1)  # unigrammes