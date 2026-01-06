from typing import List, Optional

from app.database import db
from app.entities.movie import Movie
from app.repositories.base import IMovieRepository


class SqlMovieRepository(IMovieRepository):
    def save_many(self, movies: List[Movie]) -> None:
        db.session.bulk_save_objects(movies)
        db.session.commit()

    def get_by_tmdb_id(self, tmdb_id: int) -> Optional[Movie]:
        return Movie.query.filter_by(tmdb_id=tmdb_id).first()

    def get_by_id(self, movie_id: int) -> Optional[Movie]:
        return Movie.query.get(movie_id)

    def get_all(self) -> List[Movie]:
        return Movie.query.all()

    def search(
        self, query: Optional[str], page: int, per_page: int
    ) -> tuple[list[Movie], int]:
        q = Movie.query  # type: ignore
        if query:
            like = f"%{query}%"
            q = q.filter(
                (Movie.title.ilike(like)) | (Movie.original_title.ilike(like))  # type: ignore
            )
        pagination = q.order_by(Movie.id.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return list(pagination.items), pagination.pages

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

        query = query.order_by(Movie.vote_count.desc(), Movie.vote_average.desc())  # type: ignore
        return query.all()
