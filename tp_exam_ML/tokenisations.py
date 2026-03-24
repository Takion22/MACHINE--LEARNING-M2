import re
from corpus import get_wikipedia_mg_text

# Fonction de tokenisation

def tokenisation(text):
    # Convertir les majuscules en minuscules
    text = text.lower()
    
    # Garder uniquement les lettres et apostrophes qui sont courants en malagasy
    text = re.sub(r"[^a-zàâéèêëîïôùûüç'\s]", " ", text)
    
    # Découper sur les espaces et retours à la ligne
    tokens = text.split()
    
    return tokens

tokens = tokenisation(get_wikipedia_mg_text("Madagasikara")) #+ " " + get_wikipedia_mg_text("Tantara") + " " + get_wikipedia_mg_text("Politika") + " " + get_wikipedia_mg_text("Siansa") + " " + get_wikipedia_mg_text("Kolontsaina") + " " + get_wikipedia_mg_text("Ekonomia") + " " + get_wikipedia_mg_text("Fampianarana") + " " + get_wikipedia_mg_text("Siansa") + " " + get_wikipedia_mg_text("Fomba_fomba") + " " + get_wikipedia_mg_text("Fiarahamonina") + " " + get_wikipedia_mg_text("Toekarena") + " " + get_wikipedia_mg_text("Fanabeazana"))
# print(tokens)
# ["ny", "vary", "masaka", "tsara", "ny", "olona", ...]