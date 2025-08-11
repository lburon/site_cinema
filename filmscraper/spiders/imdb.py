import requests
from bs4 import BeautifulSoup

def get_imdb_id(movie_name):
    query = movie_name.replace(" ", "+")
    search_url = f"https://www.imdb.com/find/?q={query}&s=tt&ttype=ft"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Cherche le premier lien de film dans la liste
    first_result = soup.select_one("ul.ipc-metadata-list a")
    if first_result and "/title/" in first_result["href"]:
        return first_result["href"].split("/")[2]  # Récupère l'ID ex: tt1375666
    return None

def get_imdb_rating(movie_id):
    movie_url = f"https://www.imdb.com/title/{movie_id}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(movie_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    rating_tag = soup.select_one('[data-testid="hero-rating-bar__aggregate-rating__score"] span')
    if rating_tag:
        return rating_tag.text.strip()
    return None

if __name__ == "__main__":
    movie_name = input("Nom du film : ")
    imdb_id = get_imdb_id(movie_name)
    
    if imdb_id:
        rating = get_imdb_rating(imdb_id)
        print(f"Film trouvé : {imdb_id}, Note IMDb : {rating}")
    else:
        print("Film non trouvé sur IMDb.")