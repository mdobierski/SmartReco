from typing import Optional

from app.entities.user import User
from app.repositories.base import IUserRepository
from app.utils.password_hasher import PasswordHasherService


class AuthService:

    def __init__(
        self, user_repo: IUserRepository, password_hasher: PasswordHasherService
    ):
        self.user_repo = user_repo
        self.password_hasher = password_hasher

    def register(self, email: str, password: str) -> Optional[User]:

        existing = self.user_repo.find_by_email(email)
        if existing:
            return None
        password_hash = self.password_hasher.hash_password(password)
        user = User(email=email, password_hash=password_hash)

        self.user_repo.save(user)
        return user

    def login(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.find_by_email(email)
        if not user:
            return None

        is_valid = self.password_hasher.verify_password(user.password_hash, password)
        if not is_valid:
            return None

        return user
