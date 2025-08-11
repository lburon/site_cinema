import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
import json

def slugify_letterboxd(title):
    title = unidecode(title.lower())
    # Supprime les apostrophes simples et typographiques
    title = re.sub(r"[’']", "", title)
    # Remplace tout ce qui n'est pas alphanumérique par un tiret
    title = re.sub(r"[^a-z0-9]+", "-", title)
    # Nettoie les tirets en début/fin ou multiples
    title = re.sub(r"^-+|-+$", "", title)
    title = re.sub(r"-{2,}", "-", title)
    return title


def get_letterboxd_rating(imdb_id):
    movie_url = f'https://letterboxd.com/imdb/{imdb_id}/'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}

    try:
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la requête HTTP: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", type="application/ld+json")
    if not script_tag:
        print("JSON-LD non trouvé dans la page.")
        return None

    # Nettoyer le contenu JSON en supprimant les commentaires CDATA
    raw_json = script_tag.string.strip()
    # Supprimer /* <![CDATA[ */ et /* ]]> */
    raw_json = re.sub(r'/\*<!\[CDATA\[\\*/', '', raw_json)
    raw_json = re.sub(r'/\*\s*\]\]>\s*\*/', '', raw_json)
    raw_json = raw_json.strip()

    # Juste pour être sûr, on retire tout ce qui est entre /* ... */
    raw_json = re.sub(r'/\*.*?\*/', '', raw_json, flags=re.DOTALL).strip()

    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON : {e}")
        return None

    rating = None
    if "aggregateRating" in data and "ratingValue" in data["aggregateRating"]:
        rating = data["aggregateRating"]["ratingValue"]

    if rating is not None:
        return str(rating)
    else:
        print("Note non trouvée dans les données JSON-LD.")
        return None


if __name__ == "__main__":
    movie_name = input("Nom du film : ")

    rating = get_letterboxd_rating(movie_name)
    if rating:
        print(f"Note Letterboxd : {rating}")
    else:
        print("Film non trouvé sur Letterboxd.")