from flask import redirect, render_template, request, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.movie_service import MovieService
from app.services.preference_service import PreferenceService


class PreferenceController(BaseController):
    """
    Controller responsible for user preferences management.
    Responsibility: display form, save preferences.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        movie_service: MovieService,
        preference_service: PreferenceService,
    ):
        super().__init__(user_repo)
        self.movie_service = movie_service
        self.preference_service = preference_service

    def show_form(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        filter_values = self.movie_service.get_filter_values()
        return render_template("preferences.html", **filter_values)

    def save_preferences(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        countries = request.form.getlist("countries")
        genres = request.form.getlist("genres")
        year_from = request.form.get("year_from")
        year_to = request.form.get("year_to")

        self.preference_service.save_preferences(
            user_id=user_id,
            countries=countries if countries else None,
            genres=genres if genres else None,
            year_from=int(year_from) if year_from else None,
            year_to=int(year_to) if year_to else None,
        )
        return redirect(url_for("index"))
