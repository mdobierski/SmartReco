from typing import Optional

from flask import redirect, session, url_for

from app.repositories.base import IUserRepository


class BaseController:
    """
    Klasa bazowa dla wszystkich kontrolerów.
    Odpowiedzialność: wspólna logika (auth, user_id, redirects).
    """

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_current_user_id(self) -> Optional[int]:
        email = session.get("user_email")
        if not email:
            return None
        user = self.user_repo.find_by_email(email)
        return user.id if user else None

    def is_authenticated(self) -> bool:
        return "user_email" in session

    def require_auth(self):
        if not self.is_authenticated():
            return redirect(url_for("login"))
        return None

    def get_current_email(self) -> Optional[str]:
        return session.get("user_email")
