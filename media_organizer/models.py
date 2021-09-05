import uuid
from typing import List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, Session, SQLModel


class SpokenLanguageMovieLink(SQLModel, table=True):
    spoken_language_id: Optional[UUID] = Field(
        default=None, foreign_key="spoken_language.local_id", primary_key=True
    )
    movie_id: Optional[UUID] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class SpokenLanguage(SQLModel, table=True):
    __tablename__ = "spoken_language"
    local_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    english_name: str
    iso_639_1: str
    name: str
    movies: List["Movie"] = Relationship(
        back_populates="spoken_languages", link_model=SpokenLanguageMovieLink
    )


class ProductionCountryMovieLink(SQLModel, table=True):
    production_country_id: Optional[UUID] = Field(
        default=None, foreign_key="production_country.local_id", primary_key=True
    )
    movie_id: Optional[UUID] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class ProductionCountry(SQLModel, table=True):
    __tablename__ = "production_country"
    local_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    iso_3166_1: str
    name: str
    movies: List["Movie"] = Relationship(
        back_populates="production_countries", link_model=ProductionCountryMovieLink
    )


class ProductionCompanyMovieLink(SQLModel, table=True):
    production_company_id: Optional[UUID] = Field(
        default=None, foreign_key="production_company.local_id", primary_key=True
    )
    movie_id: Optional[UUID] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class ProductionCompany(SQLModel, table=True):
    __tablename__ = "production_company"
    local_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: int
    name: str
    origin_country: str
    logo_path: Optional[str] = None
    movies: List["Movie"] = Relationship(
        back_populates="production_companies", link_model=ProductionCompanyMovieLink
    )


class Collection(SQLModel, table=True):
    local_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: int
    name: str
    poster_path: str
    backdrop_path: str
    movies: List["Movie"] = Relationship(back_populates="collection")


class GenreMovieLink(SQLModel, table=True):
    genre_id: Optional[UUID] = Field(
        default=None, foreign_key="genre.local_id", primary_key=True
    )
    movie_id: Optional[UUID] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class Genre(SQLModel, table=True):
    local_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id: int
    name: str
    movies: List["Movie"] = Relationship(
        back_populates="genres", link_model=GenreMovieLink
    )


class Movie(SQLModel, table=True):
    local_id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    adult: bool
    backdrop_path: str
    collection_id: Optional[UUID] = Field(
        default=None, foreign_key="collection.local_id"
    )
    collection: Optional[Collection] = Relationship(back_populates="movies")
    budget: int
    genres: List[Genre] = Relationship(
        back_populates="movies", link_model=GenreMovieLink
    )
    homepage: str
    id: int
    imdb_id: str
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    production_companies: List[ProductionCompany] = Relationship(
        back_populates="movies", link_model=ProductionCompanyMovieLink
    )
    production_countries: List[ProductionCountry] = Relationship(
        back_populates="movies", link_model=ProductionCountryMovieLink
    )
    release_date: str = Field(..., index=True)
    revenue: int
    runtime: int
    spoken_languages: List[SpokenLanguage] = Relationship(
        back_populates="movies", link_model=SpokenLanguageMovieLink
    )
    status: str
    tagline: str
    title: str = Field(..., index=True)
    video: bool
    vote_average: float
    vote_count: int


def create_model_obj(o: dict, model_type: SQLModel, session: Session) -> SQLModel:
    obj = model_type(**o)
    # session.add(obj)
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
