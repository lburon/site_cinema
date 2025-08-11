from flask import Flask, request, render_template_string
from filmscraper.spiders.letterboxd import slugify_letterboxd, get_letterboxd_rating
from filmscraper.spiders.omdb import get_all_ratings

app = Flask(__name__)

API_KEY = "206dfa40"

HTML = """
<!doctype html>
<title>Notes de film</title>
<h1>Recherche de notes</h1>
<form method="post">
  <input name="movie_name" placeholder="Nom du film" required>
  <input type="submit" value="Chercher">
</form>
{% if ratings %}
  <h2>Résultats pour "{{ movie_name }}" :</h2>
  <ul>
    <li>Letterboxd : {{ letterboxd or "N/A" }}</li>
    <li>IMDb : {{ ratings.get('Internet Movie Database', 'N/A') }}</li>
    <li>Rotten Tomatoes : {{ ratings.get('Rotten Tomatoes', 'N/A') }}</li>
    <li>Metacritic : {{ ratings.get('Metacritic', 'N/A') }}</li>
  </ul>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    ratings = {}
    letterboxd = None
    movie_name = ""
    if request.method == "POST":
        movie_name = request.form["movie_name"]
        letterboxd_name = slugify_letterboxd(movie_name)
        letterboxd = get_letterboxd_rating(letterboxd_name)
        ratings = get_all_ratings(movie_name, API_KEY)
    return render_template_string(HTML, ratings=ratings, letterboxd=letterboxd, movie_name=movie_name)

if __name__ == "__main__":
    app.run(debug=True)