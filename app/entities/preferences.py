from datetime import datetime, timezone
from typing import Optional

from app.database import db


class Preferences(db.Model):
    """
    Model preferencji użytkownika.
    Reprezentuje tabelę 'preferences' w bazie danych.
    """

    __tablename__ = "preferences"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    countries = db.Column(db.JSON)
    genres = db.Column(db.JSON)
    year_from = db.Column(db.Integer, nullable=True)
    year_to = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = db.relationship("User", back_populates="preferences")

    def __init__(
        self,
        user_id: int,
        countries: Optional[list[str]] = None,
        genres: Optional[list[str]] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> None:
        super().__init__()
        self.user_id = user_id
        self.countries = countries
        self.genres = genres
        self.year_from = year_from
        self.year_to = year_to

    def __repr__(self) -> str:
        return f"<Preferences user_id={self.user_id}>"
