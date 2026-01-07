from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.movie import Movie
from app.entities.preferences import Preferences
from app.entities.rating import Rating
from app.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def save(self, user: User) -> None: ...


class IMovieRepository(ABC):
    @abstractmethod
    def save_many(self, movies: List[Movie]) -> None: ...

    @abstractmethod
    def get_by_tmdb_id(self, tmdb_id: int) -> Optional[Movie]: ...

    @abstractmethod
    def get_by_id(self, movie_id: int) -> Optional[Movie]: ...

    @abstractmethod
    def get_all(self) -> List[Movie]: ...

    @abstractmethod
    def search(
        self, query: Optional[str], page: int, per_page: int
    ) -> tuple[list[Movie], int]: ...

    @abstractmethod
    def get_distinct_countries(self) -> List[str]: ...

    @abstractmethod
    def get_distinct_genres(self) -> List[str]: ...

    @abstractmethod
    def filter_movies(
        self,
        countries: List[str],
        genres: List[str],
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> List[Movie]: ...


class IRatingRepository(ABC):
    @abstractmethod
    def save(self, rating: Rating) -> None: ...

    @abstractmethod
    def get_user_ratings(self, user_id: int) -> List[Rating]: ...

    @abstractmethod
    def get_user_rating(self, user_id: int, movie_id: int) -> Optional[Rating]: ...

    @abstractmethod
    def get_ratings_for_movie(self, movie_id: int) -> List[Rating]: ...

    @abstractmethod
    def delete_rating(self, user_id: int, movie_id: int) -> bool: ...

    @abstractmethod
    def get_user_ratings_with_movies(self, user_id: int, search: str = "") -> list: ...


class IPreferencesRepository(ABC):
    @abstractmethod
    def upsert(self, prefs: Preferences) -> None: ...

    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Preferences]: ...
