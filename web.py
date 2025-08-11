from flask import Flask, request, render_template_string
from filmscraper.spiders.letterboxd import slugify_letterboxd, get_letterboxd_rating
from filmscraper.spiders.omdb import get_all_ratings

app = Flask(__name__)

API_KEY = "206dfa40"

HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Movie Ratings</title>
  <style>
    body {
      background-color: #121417;  /* very dark background */
      color: #ecf0f1;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0; padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }
    h1 {
      margin-top: 40px;
      font-size: 2.5rem;
      font-weight: 700;
    }
    h2 {
      margin-top: 40px;
      font-size: 1.5rem;  /* taille plus petite */
    }
    form {
      margin: 30px 0;
      display: flex;
      justify-content: center;
      width: 100%;
      max-width: 400px;
    }
    input[name="movie_name"] {
      flex-grow: 1;
      padding: 12px 15px;
      font-size: 1.2rem;
      border: none;
      border-radius: 5px 0 0 5px;
      outline: none;
    }
    input[type="submit"] {
      padding: 12px 20px;
      font-size: 1.2rem;
      border: none;
      background-color: #3498db;
      color: white;
      cursor: pointer;
      border-radius: 0 5px 5px 0;
      transition: background-color 0.3s ease;
    }
    input[type="submit"]:hover {
      background-color: #2980b9;
    }
    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      max-width: 600px;
      width: 100%;
      font-size: 1.3rem;
      display: flex;
      justify-content: space-around;
      align-items: center;
    }
    ul li {
        margin: 0 15px;
        display: flex;
        flex-direction: column;  /* stack logo and rating vertically */
        align-items: center;
        gap: 6px;
    }
    ul li img {
        width: 60px;    /* larger logos */
        height: auto;   /* keep aspect ratio */
        object-fit: contain; /* avoid distortion */
    }
    .rating-item {
        flex: 1 1 120px; /* wider min width */
        margin: 20px; /* more space between blocks */
    }
    .rating-item img {
        display: block;
        margin: 0 auto 15px;
        max-width: 80px;  /* bigger logos */
        height: auto;
    }
  </style>
</head>
<body>
  <h1>Search Movie Ratings</h1>
  <form method="post">
    <input name="movie_name" placeholder="Movie title in English" required>
    <input type="submit" value="Search">
  </form>
  
  {% if poster_url and poster_url != "N/A" %}
    <img src="{{ poster_url }}" alt="Movie Poster" style="max-width: 300px; margin-bottom: 20px; border-radius: 8px;">
  {% endif %}
  
  {% if ratings %}
    <h2>Results for "{{ movie_name }}" :</h2>
    <ul>
      <li>
        <img src="{{ url_for('static', filename='logos/letterboxd.png') }}" alt="Letterboxd">
        {{ letterboxd or "N/A" }}
      </li>
      <li>
        <img src="{{ url_for('static', filename='logos/imdb.png') }}" alt="IMDb">
        {{ ratings.get('Internet Movie Database', 'N/A') }}
      </li>
      <li>
        <img src="{{ url_for('static', filename='logos/rotten_tomatoes.png') }}" alt="Rotten Tomatoes">
        {{ ratings.get('Rotten Tomatoes', 'N/A') }}
      </li>
      <li>
        <img src="{{ url_for('static', filename='logos/metacritic.png') }}" alt="Metacritic">
        {{ ratings.get('Metacritic', 'N/A') }}
      </li>
    </ul>
  {% endif %}
</body>
</html>
"""



@app.route("/", methods=["GET", "POST"])
def index():
    ratings = {}
    letterboxd = None
    movie_name = ""
    poster_url = None
    if request.method == "POST":
        movie_name = request.form["movie_name"]
        letterboxd_name = slugify_letterboxd(movie_name)
        letterboxd = get_letterboxd_rating(letterboxd_name)
        ratings, poster_url = get_all_ratings(movie_name, API_KEY)  # maintenant deux retours

    return render_template_string(HTML, ratings=ratings, letterboxd=letterboxd, movie_name=movie_name, poster_url=poster_url)

if __name__ == "__main__":
    app.run(debug=True)