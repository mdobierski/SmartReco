from typing import Optional

from app.database import db


class Movie(db.Model):
    """
    Model filmu w systemie.
    Reprezentuje tabelę 'movies' w bazie danych.
    Zawiera dane z TMDb API.
    """

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    original_title = db.Column(db.String(500))
    year = db.Column(db.Integer, index=True)
    runtime = db.Column(db.Integer)
    overview = db.Column(db.Text)
    poster_path = db.Column(db.String(255))
    genre = db.Column(db.String(100), index=True)
    country = db.Column(db.String(100), index=True)
    director = db.Column(db.String(255))
    vote_average = db.Column(db.Float)
    vote_count = db.Column(db.Integer)

    ratings = db.relationship("Rating", back_populates="movie", lazy="write_only")

    def __init__(
        self,
        tmdb_id: int,
        title: str,
        original_title: Optional[str] = None,
        year: Optional[int] = None,
        runtime: Optional[int] = None,
        overview: Optional[str] = None,
        poster_path: Optional[str] = None,
        genre: Optional[str] = None,
        country: Optional[str] = None,
        director: Optional[str] = None,
        vote_average: Optional[float] = None,
        vote_count: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.tmdb_id = tmdb_id
        self.title = title
        self.original_title = original_title
        self.year = year
        self.runtime = runtime
        self.overview = overview
        self.poster_path = poster_path
        self.genre = genre
        self.country = country
        self.director = director
        self.vote_average = vote_average
        self.vote_count = vote_count

    def __repr__(self) -> str:
        return f"<Movie {self.title} ({self.year})>"
