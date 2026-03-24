import requests

def get_wikipedia_mg_text(title):
    url = f"https://mg.wikipedia.org/w/api.php"
    params = {
        "action" : "query",
        "titles" : title,
        "prop" : "extracts",
        "explaintext" : True,
        "format" : "json"
    }
    headers = {"User-Agent": "CorpusScript/1.0"}
    response = requests.get(url, params=params, headers=headers)
    pages = response.json()["query"]["pages"]
    return list(pages.values())[0].get("extract", "")

# Exemple : récupérer plusieurs articles
# articles = ["Madagasikara", "Tantara", "Politika"]
# corpus = " ".join([get_wikipedia_mg_text(t) for t in articles])
# print(corpus)