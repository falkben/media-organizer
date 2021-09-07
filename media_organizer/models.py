from datetime import date
from typing import List, Optional

from rich.console import Console, ConsoleOptions, RenderResult
from rich.text import Text
from sqlmodel import Field, Relationship, SQLModel


class SpokenLanguageMovieLink(SQLModel, table=True):
    spoken_language_id: Optional[int] = Field(
        default=None, foreign_key="spoken_language.local_id", primary_key=True
    )
    movie_id: Optional[int] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class SpokenLanguage(SQLModel, table=True):
    __tablename__ = "spoken_language"
    local_id: Optional[int] = Field(default=None, primary_key=True)
    english_name: Optional[str] = None
    iso_639_1: Optional[str] = None
    name: str
    movies: List["Movie"] = Relationship(
        back_populates="spoken_languages", link_model=SpokenLanguageMovieLink
    )

    def __rich_repr__(self):
        yield self.name


class ProductionCountryMovieLink(SQLModel, table=True):
    production_country_id: Optional[int] = Field(
        default=None, foreign_key="production_country.local_id", primary_key=True
    )
    movie_id: Optional[int] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class ProductionCountry(SQLModel, table=True):
    __tablename__ = "production_country"
    local_id: Optional[int] = Field(default=None, primary_key=True)
    iso_3166_1: Optional[str] = None
    name: str
    movies: List["Movie"] = Relationship(
        back_populates="production_countries", link_model=ProductionCountryMovieLink
    )

    def __rich_repr__(self):
        yield self.name


class ProductionCompanyMovieLink(SQLModel, table=True):
    production_company_id: Optional[int] = Field(
        default=None, foreign_key="production_company.local_id", primary_key=True
    )
    movie_id: Optional[int] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class ProductionCompany(SQLModel, table=True):
    __tablename__ = "production_company"
    local_id: Optional[int] = Field(default=None, primary_key=True)
    id: int
    name: str
    origin_country: Optional[str] = None
    logo_path: Optional[str] = None
    movies: List["Movie"] = Relationship(
        back_populates="production_companies", link_model=ProductionCompanyMovieLink
    )

    def __rich_repr__(self):
        yield self.name


class Collection(SQLModel, table=True):
    local_id: Optional[int] = Field(default=None, primary_key=True)
    id: int
    name: str
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    movies: List["Movie"] = Relationship(back_populates="collection")

    def __rich_repr__(self):
        yield self.name


class GenreMovieLink(SQLModel, table=True):
    genre_id: Optional[int] = Field(
        default=None, foreign_key="genre.local_id", primary_key=True
    )
    movie_id: Optional[int] = Field(
        default=None, foreign_key="movie.local_id", primary_key=True
    )


class Genre(SQLModel, table=True):
    local_id: Optional[int] = Field(default=None, primary_key=True)
    id: int
    name: str
    movies: List["Movie"] = Relationship(
        back_populates="genres", link_model=GenreMovieLink
    )

    def __rich_repr__(self):
        yield self.name


class Movie(SQLModel, table=True):
    local_id: Optional[int] = Field(default=None, primary_key=True)
    adult: Optional[bool] = None
    backdrop_path: Optional[str] = None
    collection_id: Optional[int] = Field(
        default=None, foreign_key="collection.local_id"
    )
    collection: Optional[Collection] = Relationship(back_populates="movies")
    budget: Optional[int] = None
    genres: List[Genre] = Relationship(
        back_populates="movies", link_model=GenreMovieLink
    )
    homepage: Optional[str] = None
    id: int
    imdb_id: Optional[str] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    production_companies: List[ProductionCompany] = Relationship(
        back_populates="movies", link_model=ProductionCompanyMovieLink
    )
    production_countries: List[ProductionCountry] = Relationship(
        back_populates="movies", link_model=ProductionCountryMovieLink
    )
    release_date: Optional[date] = Field(None, index=True)
    revenue: Optional[int] = None
    runtime: Optional[int] = None
    spoken_languages: List[SpokenLanguage] = Relationship(
        back_populates="movies", link_model=SpokenLanguageMovieLink
    )
    status: Optional[str] = None
    tagline: Optional[str] = None
    title: str = Field(..., index=True)
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

    def __rich_repr__(self):
        yield self.title
        yield "overview", self.overview
        yield "release_date", self.release_date
        yield "runtime", f"{self.runtime} min"
        yield "genres", self.genres
        yield "collection", self.collection
        yield "spoken_languages", self.spoken_languages
        yield "revenue", f"{self.revenue / 1e6:.1f}M"

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        yield Text(f"{self.title}", justify="center", style="bold magenta")

        release_date_str = self.release_date.strftime("%b %d, %Y")
        yield Text(f"Released: {release_date_str}")
        yield Text(f"Runtime: {self.runtime} min")

        genres_str = ", ".join([g.name for g in self.genres])
        yield Text(f"Genres: {genres_str}")

        return
