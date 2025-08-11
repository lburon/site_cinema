from filmscraper.spiders.letterboxd import slugify_letterboxd, get_letterboxd_rating
from filmscraper.spiders.omdb import get_all_ratings

film = "district 9"

# LETTERBOXD
letterboxd_name = slugify_letterboxd(film)
letterboxd_rating = get_letterboxd_rating(letterboxd_name)

# ROTTEN TOMATOES, METACRITIC, IMDb
api_key = "206dfa40"
all_ratings = get_all_ratings(film, api_key)

if all_ratings :
    imdb_rating = all_ratings.get('Internet Movie Database')
    rotten_tomatoes_rating = all_ratings.get('Rotten Tomatoes')
    metacritic_rating = all_ratings.get('Metacritic')

print(f"Letterboxd : {letterboxd_rating}")
print(f"IMDb : {imdb_rating}")
print(f"Rotten Tomatoes : {rotten_tomatoes_rating}")
print(f"Metacritic : {metacritic_rating}")
