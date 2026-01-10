from typing import Optional

from flask import redirect, session, url_for

from app.repositories.base import IUserRepository


class BaseController:
    """
    Base class for all controllers.
    Responsibility: shared logic (auth, user_id, redirects).
    """

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_current_user_id(self) -> int:
        """
        Get current user ID. Should only be called after require_auth().
        """
        email = session.get("user_email")
        if not email:
            raise RuntimeError("User not authenticated - call require_auth() first")
        user = self.user_repo.find_by_email(email)
        if not user:
            raise RuntimeError(f"User with email {email} not found in database")
        return user.id

    def is_authenticated(self) -> bool:
        return "user_email" in session

    def require_auth(self):
        if not self.is_authenticated():
            return redirect(url_for("login"))
        return None

    def get_current_email(self) -> Optional[str]:
        return session.get("user_email")
