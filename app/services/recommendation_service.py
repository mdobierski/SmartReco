from typing import List, Optional

from app.entities.movie import Movie
from app.repositories.base import IMovieRepository, IPreferencesRepository


class RecommendationService:

    def __init__(
        self,
        movie_repo: IMovieRepository,
        prefs_repo: IPreferencesRepository,
    ) -> None:
        self.movie_repo = movie_repo
        self.prefs_repo = prefs_repo

    def recommend_for_user(self, user_id: int, limit: int = 20) -> List[Movie]:

        prefs = self.prefs_repo.get_by_user_id(user_id)

        if prefs is None:
            movies = self.movie_repo.filter_movies([], [], None, None)
        else:
            movies = self.movie_repo.filter_movies(
                countries=prefs.countries or [],
                genres=prefs.genres or [],
                year_from=prefs.year_from,
                year_to=prefs.year_to,
            )

        return movies[:limit]

    def recommend_with_filters(
        self,
        countries: Optional[List[str]] = None,
        genres: Optional[List[str]] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit: int = 50,
    ) -> List[Movie]:

        movies = self.movie_repo.filter_movies(
            countries=countries or [],
            genres=genres or [],
            year_from=year_from,
            year_to=year_to,
        )
        return movies[:limit]
