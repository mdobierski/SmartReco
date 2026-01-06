from typing import List, Optional

from app.database import db
from app.entities.movie import Movie
from app.repositories.base import IMovieRepository


class SqlMovieRepository(IMovieRepository):

    def save_many(self, movies: List[Movie]) -> None:
        db.session.bulk_save_objects(movies)
        db.session.commit()

    def get_by_tmdb_id(self, tmdb_id: int) -> Optional[Movie]:
        """Znajdź film po tmdb_id (zewnętrznym ID z TMDb API)."""
        return Movie.query.filter_by(tmdb_id=tmdb_id).first()

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return Movie.query.get(movie_id)

    def get_all(self) -> List[Movie]:
        return Movie.query.all()

    def get_distinct_countries(self) -> List[str]:
        rows = db.session.query(Movie.country).distinct().all()  # type: ignore
        return [r[0] for r in rows if r[0]]

    def get_distinct_genres(self) -> List[str]:
        rows = db.session.query(Movie.genre).distinct().all()  # type: ignore
        return [r[0] for r in rows if r[0]]

    def filter_movies(
        self,
        countries: List[str],
        genres: List[str],
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> List[Movie]:
        query = Movie.query  # type: ignore

        if countries:
            query = query.filter(Movie.country.in_(countries))  # type: ignore
        if genres:
            query = query.filter(Movie.genre.in_(genres))  # type: ignore
        if year_from is not None:
            query = query.filter(Movie.year >= year_from)  # type: ignore
        if year_to is not None:
            query = query.filter(Movie.year <= year_to)  # type: ignore

        # Sortuj po popularności/ocenie (tu: vote_count desc, vote_average desc)
        query = query.order_by(Movie.vote_count.desc(), Movie.vote_average.desc())  # type: ignore

        return query.all()
