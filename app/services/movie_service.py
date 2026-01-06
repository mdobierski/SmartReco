from typing import List, Optional

from app.entities.movie import Movie
from app.repositories.base import IMovieRepository


class MovieService:

    def __init__(self, movie_repo: IMovieRepository):
        self.movie_repo = movie_repo

    def get_all_movies(self) -> List[Movie]:
        return self.movie_repo.get_all()

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.movie_repo.get_by_id(movie_id)

    def get_filter_values(self):

        countries = self.movie_repo.get_distinct_countries()
        genres = self.movie_repo.get_distinct_genres()
        return {
            "countries": countries,
            "genres": genres,
        }

    def filter_movies(
        self,
        countries: List[str],
        genres: List[str],
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> List[Movie]:
        return self.movie_repo.filter_movies(countries, genres, year_from, year_to)
