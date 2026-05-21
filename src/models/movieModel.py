import requests

OMDB_API_KEY = "TU_API_KEY"

class MovieModel:
    """Model para obtener información de películas y series desde OMDb"""

    @staticmethod
    def search_movies(title):
        """
        Buscar películas o series por título.
        Devuelve una lista de resultados.
        """
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={title}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            
            if data.get('Response') == 'True':
                return data.get('Search', [])
            else:
                return []
        except requests.RequestException as e:
            print("Error al consultar OMDb:", e)
            return []

    @staticmethod
    def get_movie_details(imdb_id):
        """
        Obtener detalles completos de una película o serie por su IMDb ID.
        """
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}&plot=full"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get('Response') == 'True':
                return data
            else:
                return None
        except requests.RequestException as e:
            print("Error al obtener detalles:", e)
            return None

    @staticmethod
    def format_movie_card(movie):
        """
        Formatea la información básica para mostrar en la card de la UI.
        """
        return {
            "title": movie.get("Title"),
            "year": movie.get("Year"),
            "imdb_id": movie.get("imdbID"),
            "poster": movie.get("Poster") if movie.get("Poster") != "N/A" else "/static/default_poster.jpg",
            "type": movie.get("Type")
        }

    @staticmethod
    def get_movies_for_view(title):
        """
        Busca y formatea resultados listos para la vista.
        """
        raw_movies = MovieModel.search_movies(title)
        formatted = [MovieModel.format_movie_card(m) for m in raw_movies]
        return formatted
