from typing import Dict, List, Optional, Tuple

from app.entities.movie import Movie
from app.repositories.base import IMovieRepository


class MovieService:
    def __init__(self, movie_repo: IMovieRepository):
        self.movie_repo = movie_repo

    def get_movie(self, movie_id: int) -> Optional[Movie]:
        return self.movie_repo.get_by_id(movie_id)

    def get_filter_values(self) -> Dict[str, List[str]]:
        countries = self.movie_repo.get_distinct_countries()
        genres = self.movie_repo.get_distinct_genres()
        return {"countries": countries, "genres": genres}

    def search_paginated(
        self, query: Optional[str], page: int, per_page: int
    ) -> Tuple[List[Movie], int]:
        return self.movie_repo.search(query, page, per_page)
