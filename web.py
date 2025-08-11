from flask import Flask, request, render_template
from filmscraper.spiders.letterboxd import slugify_letterboxd, get_letterboxd_rating
import requests
import json
from mean import weighted_average

app = Flask(__name__)
API_KEY = '206dfa40'

def parse_rating(value):
    """
    Convert different rating formats to a 0-10 scale float.
    Exemple: '7.5/10' -> 7.5, '87%' -> 8.7, '74/100' -> 7.4
    """
    if value.endswith('%'):
        return float(value.strip('%')) / 10
    elif '/' in value:
        num, denom = value.split('/')
        return float(num) * 10 / float(denom)
    try:
        return float(value)
    except:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    movie_name = None
    ratings = {}
    letterboxd = None
    average = None
    poster_url = None
    details = {}
    search_results = []  # << initialisation ici

    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        selected_imdb_id = request.form.get('imdb_id')

        if movie_name and not selected_imdb_id:
            print("Recherche OMDb pour:", movie_name)  # debug
            url = f"http://www.omdbapi.com/?s={movie_name}&apikey={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Réponse OMDb:", data)  # debug
                if data.get('Response') == 'True':
                    search_results = data.get('Search', [])[:4]
                else:
                    search_results = []

        elif selected_imdb_id:
            print("Recherche détail OMDb imdbID:", selected_imdb_id)  # debug
            url = f"http://www.omdbapi.com/?i={selected_imdb_id}&apikey={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    poster_url = data.get('Poster')
                    details = {
                        'year': data.get('Year'),
                        'director': data.get('Director'),
                        'actors': data.get('Actors'),
                        'runtime': data.get('Runtime'),
                        'writer': data.get('Writer'),
                        'plot': data.get('Plot'),
                    }
                    ratings = {r['Source']: r['Value'] for r in data.get('Ratings', [])}

                    letterboxd = get_letterboxd_rating(selected_imdb_id)

                    average = weighted_average(ratings, letterboxd)

    return render_template('index.html',
                           movie_name=movie_name,
                           ratings=ratings,
                           letterboxd=letterboxd,
                           average=average,
                           poster_url=poster_url,
                           details=details,
                           search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)