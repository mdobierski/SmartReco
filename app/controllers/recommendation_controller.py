from flask import redirect, render_template, request, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.movie_service import MovieService
from app.services.preference_service import PreferenceService
from app.services.recommendation_service import RecommendationService


class RecommendationController(BaseController):
    """
    Controller for recommendations: criteria-based and personal.
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

        # After POST submission, redirect to GET endpoint with parameters
        # so pagination and links work consistently
        return redirect(
            url_for(
                "criteria_results",
                countries=countries,
                genres=genres,
                year_from=year_from,
                year_to=year_to,
                page=request.args.get("page", 1),
            )
        )

    def criteria_results(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        countries = request.args.getlist("countries")
        genres = request.args.getlist("genres")
        year_from = request.args.get("year_from")
        year_to = request.args.get("year_to")
        page = int(request.args.get("page", 1))

        movies, total_pages = self.recommendation_service.recommend_with_filters(
            countries=countries if countries else None,
            genres=genres if genres else None,
            year_from=int(year_from) if year_from else None,
            year_to=int(year_to) if year_to else None,
            page=page,
        )

        return render_template(
            "recommendations.html",
            movies=movies,
            rec_type="Criteria",
            percents=[],  # Empty for criteria
            page=page,
            total_pages=total_pages,
            countries=countries,
            genres=genres,
            year_from=year_from,
            year_to=year_to,
        )

    def personal_recommend(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        prefs = self.preference_service.get_preferences(user_id)
        if not prefs:
            return redirect(url_for("preferences"))

        page = int(request.args.get("page", 1))
        movies, total_pages, percents = self.recommendation_service.recommend_for_user(
            user_id=user_id, page=page
        )

        return render_template(
            "recommendations.html",
            movies=movies,
            rec_type="Personal",
            percents=percents,
            page=page,
            total_pages=total_pages,
        )

    def ai_coming_soon(self):
        """Display AI recommendations coming soon page."""
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        return render_template("ai_coming_soon.html")
