import re
import csv

class MalagasyRuleChecker:
    def __init__(self, dataset_path=None):
        self.vocabulary = set()
        if dataset_path:
            self.load_vocabulary(dataset_path)

    def load_vocabulary(self, path):
        """Charge le CSV pour la vérification par dictionnaire"""
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'mot' in row:
                        self.vocabulary.add(row['mot'].lower().strip())
        except Exception:
            pass 

    def is_legal(self, word):
        """
        Retourne True ou False.
        Si False, le front-end souligne en rouge.
        """
        w = word.lower().strip()
        
        # Nettoyage de la ponctuation résiduelle autour du mot
        w = re.sub(r'[^\w\s-]', '', w)
        
        if not w: return True

        # 1. Vérification par dictionnaire
        if w in self.vocabulary:
            return True
            
        # 2. Règles Phonotactiques (Combinaisons interdites)
        forbidden = ['nb', 'mk', 'dt', 'bp', 'sz']
        if any(pattern in w for pattern in forbidden):
            return False
            
        if w.startswith('nk'):
            return False

        # 3. Structure de terminaison (Voyelle ou na, ka, tra)
        if not re.search(r'[aeiouy]$|na$|ka$|tra$', w):
            return False

        return True

def run_test(user_input):
    checker = MalagasyRuleChecker("teny_wikipedia.csv")
    
    # On sépare la phrase en liste de mots
    input_words = user_input.split()
    
    results = {}
    for w in input_words:
        results[w] = checker.is_legal(w)
    
    return results

# if __name__ == "__main__":
#     phrase = input(" ")
    
#     bilan = run_test(phrase)
    
#     for mot, status in bilan.items():
#         label = "VALIDE" if status else "ERREUR"
#         print(f"[{status}] {mot} -> {label}")