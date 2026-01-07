from flask import redirect, render_template, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.preference_service import PreferenceService


class HomeController(BaseController):
    """
    Controller responsible for the home page.
    Responsibility: display home page after login.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        preference_service: PreferenceService,
    ):
        super().__init__(user_repo)
        self.preference_service = preference_service

    def index(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        prefs = self.preference_service.get_preferences(user_id)
        if not prefs:
            return redirect(url_for("preferences"))

        return render_template("home.html", email=self.get_current_email())
