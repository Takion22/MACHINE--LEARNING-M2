import pandas as pd
from langdetect import detect, DetectorFactory
import os

# Pour rendre la détection de langue reproductible
DetectorFactory.seed = 0

# ---------- CONFIG ----------
INPUT_FILE = "data/spam_raw.csv"
OUTPUT_FILE = "dataset/spam_sms_fr.csv"

TEXT_COLUMN = "text"     # ou "message"
LABEL_COLUMN = "label"   # ou "spam", "class", etc.
# ----------------------------

def is_french(text):
    """
    Retourne True si le texte est détecté comme français
    """
    try:
        return detect(str(text)) == "fr"
    except:
        return False


def normalize_label(label):
    """
    Normalise les labels en HAM / SPAM
    """
    label = str(label).lower()

    if label in ["spam", "1"]:
        return "SPAM"
    else:
        return "HAM"


def main():
    # Charger le dataset brut
    df = pd.read_csv(INPUT_FILE)

    # Renommer la colonne texte si besoin
    df = df.rename(columns={TEXT_COLUMN: "message"})

    # 1️⃣ Filtrer uniquement les messages en français
    df = df[df["message"].apply(is_french)]

    # 2️⃣ Normaliser les labels HAM / SPAM
    df["label"] = df[LABEL_COLUMN].apply(normalize_label)

    # 3️⃣ Garder uniquement les colonnes utiles
    df_final = df[["message", "label"]]

    # 4️⃣ Créer le dossier de sortie si nécessaire
    os.makedirs("dataset", exist_ok=True)

    # 5️⃣ Sauvegarder le CSV final
    df_final.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8"
    )

    print("✅ Dataset SMS SPAM français créé avec succès")
    print(df_final["label"].value_counts())


if __name__ == "__main__":
    main()
