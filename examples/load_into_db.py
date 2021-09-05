import json
import os
from pathlib import Path

import tmdbsimple as tmdb
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from media_organizer.models import tmdb_info_to_movie

load_dotenv(".env")

dbfile = Path("database.db")
if dbfile.exists():
    dbfile.unlink()
engine = create_engine("sqlite:///database.db", echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def load_movie_info_example():
    example_movie_info_file = Path("example_movie_info.json")
    if example_movie_info_file.exists():
        with open(example_movie_info_file) as fp:
            info = json.load(fp)
    else:
        tmdb.API_KEY = os.getenv("TMDB_API_KEY", None)
        movie_tmdb = tmdb.Movies(603)
        info = movie_tmdb.info()
        # store example movie data
        with open(example_movie_info_file, "w") as fp:
            json.dump(info, fp)
    return info


def main():
    create_db_and_tables()

    info = load_movie_info_example()

    # read movie info into local database
    with Session(engine) as session:
        movie = tmdb_info_to_movie(info, session)
        print(movie)


if __name__ == "__main__":
    main()
