import os

import tmdbsimple as tmdb
from dotenv import load_dotenv

load_dotenv()

tmdb.API_KEY = os.getenv("TMDB_API_KEY", None)
movie = tmdb.Movies(603)
response = movie.info()
print("Movie title:", movie.title)
