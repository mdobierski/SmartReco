from flask import redirect, render_template, request, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.movie_service import MovieService
from app.services.preference_service import PreferenceService
from app.services.recommendation_service import RecommendationService


class RecommendationController(BaseController):
    """
    Kontroler odpowiedzialny za rekomendacje filmów.
    Odpowiedzialność: rekomendacje kryterialne i personalizowane.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        movie_service: MovieService,
        preference_service: PreferenceService,
        recommendation_service: RecommendationService,
    ):
        super().__init__(user_repo)
        self.movie_service = movie_service
        self.preference_service = preference_service
        self.recommendation_service = recommendation_service

    def criteria_form(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        filter_values = self.movie_service.get_filter_values()
        return render_template("criteria.html", **filter_values)

    def criteria_recommend(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        countries = request.form.getlist("countries")
        genres = request.form.getlist("genres")
        year_from = request.form.get("year_from")
        year_to = request.form.get("year_to")

        recommended = self.recommendation_service.recommend_with_filters(
            countries=countries if countries else None,
            genres=genres if genres else None,
            year_from=int(year_from) if year_from else None,
            year_to=int(year_to) if year_to else None,
            limit=50,
        )

        return render_template(
            "recommendations.html", movies=recommended, rec_type="Criteria"
        )

    def personal_recommend(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("login"))

        prefs = self.preference_service.get_preferences(user_id)
        if not prefs:
            return redirect(url_for("preferences"))

        recommended = self.recommendation_service.recommend_for_user(user_id, limit=20)

        return render_template(
            "recommendations.html", movies=recommended, rec_type="Personal"
        )
