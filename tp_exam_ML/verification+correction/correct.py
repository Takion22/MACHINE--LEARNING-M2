import csv
from verification import MalagasyRuleChecker

class MalagasyCorrector:
    def __init__(self, dataset_path):
        self.checker = MalagasyRuleChecker(dataset_path)
        self.vocabulary = []
        self.load_vocabulary(dataset_path)

    def load_vocabulary(self, path):
        """Charge les mots du CSV pour la comparaison de distance"""
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.vocabulary = [row['mot'].lower().strip() for row in reader if 'mot' in row]
        except Exception:
            pass

    def _levenshtein(self, s1, s2):
        """Calcul de distance entre deux chaînes"""
        if len(s1) < len(s2): return self._levenshtein(s2, s1)
        if len(s2) == 0: return len(s1)
        prev = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr = [i + 1]
            for j, c2 in enumerate(s2):
                curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
            prev = curr
        return prev[-1]

    def get_correction(self, word):
        """
        Combine la vérification des règles et la recherche de suggestion.
        Retourne (is_valid, suggestion_ou_mot)
        """
        w = word.lower().strip()
        
        if self.checker.is_legal(w) and w in self.vocabulary:
            return True, w

        best_match = None
        min_dist = float('inf')

        for v in self.vocabulary:
            if abs(len(v) - len(w)) <= 2:
                dist = self._levenshtein(w, v)
                if dist < min_dist:
                    min_dist = dist
                    best_match = v
                if min_dist == 1: break

        suggestion = best_match if (best_match and min_dist < 3) else "Aucune suggestion"
        return False, suggestion

if __name__ == "__main__":
    # Point d'entrée du programme
    FILE_PATH = "teny_wikipedia.csv"
    corrector = MalagasyCorrector(FILE_PATH)
    
    print("--- Correcteur Orthographique Malagasy ---")
    user_input = input("Entrez un mot : ")
    
    is_valid, result = corrector.get_correction(user_input)
    
    if is_valid:
        print(f"{user_input}' est valide.")
    else:
        print(f"'{user_input}' est incorrect.")
        print(f"Suggestion : {result}")