from typing import Optional

from app.database import db
from app.entities.user import User
from app.repositories.base import IUserRepository


class SqlUserRepository(IUserRepository):

    def find_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def save(self, user: User) -> None:
        db.session.add(user)
        db.session.commit()
