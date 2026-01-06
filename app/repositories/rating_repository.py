from typing import List, Optional

from app.database import db
from app.entities.rating import Rating
from app.repositories.base import IRatingRepository


class SqlRatingRepository(IRatingRepository):

    def save(self, rating: Rating) -> None:
        existing = Rating.query.filter_by(
            user_id=rating.user_id, movie_id=rating.movie_id
        ).first()
        if existing:
            existing.rating = rating.rating
        else:
            db.session.add(rating)
        db.session.commit()

    def get_user_ratings(self, user_id: int) -> List[Rating]:
        return Rating.query.filter_by(user_id=user_id).all()

    def get_user_rating(self, user_id: int, movie_id: int) -> Optional[Rating]:
        return Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
