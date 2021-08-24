import os
import re
from pathlib import Path

import tmdbsimple as tmdb
from dotenv import load_dotenv

load_dotenv()

tmdb.API_KEY = os.getenv("TMDB_API_KEY", None)

movies_path = Path(os.getenv("MOVIES_FILEPATH", None))
pattern = re.compile(r"(\s\(\d{4}\))")


for movie_path in movies_path.glob("**/*"):
    movie_name = movie_path.stem

    year = None
    match = pattern.search(movie_name)
    if match:
        year = match.group().strip(" ()")
        movie_name = movie_name.replace(match.group(), "")

    search = tmdb.Search()
    response = search.movie(query=movie_name, year=year)
    for s in search.results:
        print(movie_name)
        print(s["title"], s["id"], s["release_date"])
        # store in sqlite
        break
