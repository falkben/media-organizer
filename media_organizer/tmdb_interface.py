import os
import re
from pathlib import Path
from typing import List, Optional

import tmdbsimple as tmdb
from dotenv import load_dotenv
from models import (
    Collection,
    Genre,
    Movie,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
)
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, SQLModel, select

load_dotenv()

YEAR_PATTERN = re.compile(r"(\s\(\d{4}\))")


def create_model_obj(o: dict, model_type: SQLModel, session: Session) -> SQLModel:
    obj = model_type(**o)
    return obj


def create_model_objs(
    data: dict, model_type: SQLModel, session: Session
) -> List[SQLModel]:
    objs = []
    for o in data:
        obj = create_model_obj(o, model_type, session)
        objs.append(obj)
    return objs


def tmdb_info_to_movie(info: dict, session: Session) -> Movie:
    relationship_keys = {
        "genres",
        "belongs_to_collection",
        "production_companies",
        "production_countries",
        "spoken_languages",
    }
    movie_info = {k: v for k, v in info.items() if k not in relationship_keys}

    genres = create_model_objs(info["genres"], Genre, session)

    collection = None
    if info["belongs_to_collection"]:
        collection = create_model_obj(
            info["belongs_to_collection"], Collection, session
        )

    production_companies = create_model_objs(
        info["production_companies"], ProductionCompany, session
    )

    production_countries = create_model_objs(
        info["production_countries"], ProductionCountry, session
    )

    # languages
    spoken_languages = create_model_objs(
        info["spoken_languages"], SpokenLanguage, session
    )

    # create movie
    movie = Movie(**movie_info)
    movie.genres = genres
    movie.collection = collection
    movie.production_companies = production_companies
    movie.production_countries = production_countries
    movie.spoken_languages = spoken_languages

    session.add(movie)
    session.commit()
    session.refresh(movie)

    return movie


tmdb.API_KEY = os.getenv("TMDB_API_KEY", None)


def split_movie_path_title_and_year(path: str):
    movie_path = Path(path)
    movie_name = movie_path.stem

    year = None
    match = YEAR_PATTERN.search(movie_name)
    if match:
        year = match.group().strip(" ()")
        movie_name = movie_name.replace(match.group(), "")

    return movie_name, year


def get_movie_from_path(path: str, session: Session) -> Optional[Movie]:
    movie = None

    movie_name, year = split_movie_path_title_and_year(path)

    # lookup in db
    try:
        movie = session.exec(select(Movie).where(Movie.title == movie_name)).one()
    except NoResultFound:

        search = tmdb.Search()
        search.movie(query=movie_name, year=year)
        # take the first result:
        if search.results:
            id = search.results[0]["id"]
            info = tmdb.Movies(id).info()
            movie = tmdb_info_to_movie(info, session)

    return movie
