from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordHasherService:
    """
    Serwis do hashowania i weryfikacji haseł używając Argon2.

    """

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify_password(self, password_hash: str, password: str) -> bool:
        try:
            self._hasher.verify(password_hash, password)
            return True
        except VerifyMismatchError:
            return False
