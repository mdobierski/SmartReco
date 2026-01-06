from datetime import datetime, timezone

from app.database import db


class Rating(db.Model):
    """
    Model oceny filmu przez użytkownika.
    Reprezentuje tabelę 'ratings' w bazie danych.
    """

    __tablename__ = "ratings"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="ratings")
    movie = db.relationship("Movie", back_populates="ratings")

    def __init__(self, user_id: int, movie_id: int, rating: int) -> None:
        super().__init__()
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

    def __repr__(self) -> str:
        return f"<Rating user_id={self.user_id} movie_id={self.movie_id} rating={self.rating}>"
