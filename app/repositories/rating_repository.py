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

    def get_ratings_for_movie(self, movie_id: int) -> List[Rating]:
        return Rating.query.filter_by(movie_id=movie_id).all()

    def delete_rating(self, user_id: int, movie_id: int) -> bool:
        rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if rating:
            db.session.delete(rating)
            db.session.commit()
            return True
        return False

    def get_user_ratings_with_movies(self, user_id: int, search: str = "") -> list:
        from app.entities.movie import Movie

        query = (
            db.session.query(Rating, Movie)
            .join(Movie, Rating.movie_id == Movie.id)
            .filter(Rating.user_id == user_id)  # type: ignore
        )

        if search:
            query = query.filter(Movie.title.ilike(f"%{search}%"))  # type: ignore

        results = query.order_by(Rating.created_at.desc()).all()  # type: ignore
        return results
