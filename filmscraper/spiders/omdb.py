import requests
from bs4 import BeautifulSoup
import json
import re
from unidecode import unidecode
from urllib.parse import quote_plus

def get_all_ratings(movie_name, api_key):
    query = quote_plus(movie_name)  # encode le titre pour URL
    url = f"http://www.omdbapi.com/?t={query}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Erreur API OMDb: {e}")
        return None, None, None  # modifié pour renvoyer 3 valeurs

    ratings = {}
    if "Ratings" in data:
        for rating in data["Ratings"]:
            source = rating["Source"]
            value = rating["Value"]
            ratings[source] = value

    poster_url = data.get("Poster")

    details = {
        "year": data.get("Year", "N/A"),
        "director": data.get("Director", "N/A"),
        "actors": data.get("Actors", "N/A")
    }

    return ratings, poster_url, details


if __name__ == "__main__":
    movie_name = input("Nom du film : ")
    api_key = "206dfa40"
    ratings = get_all_ratings(movie_name, api_key)
    if ratings:
        for source, value in ratings.items():
            print(f"{source} : {value}")
    else:
        print("Pas de notes trouvées.")