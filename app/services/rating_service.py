from typing import Dict, Optional

from app.entities.rating import Rating
from app.repositories.base import IRatingRepository


class RatingService:
    def __init__(self, rating_repo: IRatingRepository):
        self.rating_repo = rating_repo

    def rate_movie(self, user_id: int, movie_id: int, rating_value: int) -> None:
        if rating_value < 0 or rating_value > 10:
            raise ValueError("Rating must be between 0 and 10")
        rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating_value)
        self.rating_repo.save(rating)

    def get_user_ratings(self, user_id: int) -> Dict[int, int]:
        ratings = self.rating_repo.get_user_ratings(user_id)
        return {r.movie_id: r.rating for r in ratings}

    def get_user_rating(self, user_id: int, movie_id: int) -> Optional[int]:
        r = self.rating_repo.get_user_rating(user_id, movie_id)
        return r.rating if r else None
