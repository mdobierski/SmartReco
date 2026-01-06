from datetime import datetime, timezone

from app.database import db


class User(db.Model):
    """
    Model użytkownika w systemie.
    Reprezentuje tabelę 'users' w bazie danych.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    ratings = db.relationship("Rating", back_populates="user", lazy="write_only")
    preferences = db.relationship("Preferences", back_populates="user", uselist=False)

    def __init__(self, email: str, password_hash: str) -> None:
        super().__init__()
        self.email = email
        self.password_hash = password_hash

    def __repr__(self) -> str:
        return f"<User {self.email}>"
