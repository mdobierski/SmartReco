from flask import redirect, render_template, request, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService


class MovieController(BaseController):
    """
    Kontroler odpowiedzialny za wyświetlanie filmów i ocenianie.
    Odpowiedzialność: lista filmów, ocenianie przez użytkownika.
    """

    def __init__(
        self,
        user_repo: IUserRepository,
        movie_service: MovieService,
        rating_service: RatingService,
    ):
        super().__init__(user_repo)
        self.movie_service = movie_service
        self.rating_service = rating_service

    def list_movies(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("login"))

        movies_list = self.movie_service.get_all_movies()
        user_ratings = self.rating_service.get_user_ratings(user_id)

        return render_template(
            "movies.html", movies=movies_list, user_ratings=user_ratings
        )

    def rate_movie(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()
        if not user_id:
            return redirect(url_for("login"))

        movie_id = request.form.get("movie_id")
        rating_value = request.form.get("rating")

        if not movie_id or not rating_value:
            return "Brak wymaganych parametrów", 400

        try:
            self.rating_service.rate_movie(user_id, int(movie_id), int(rating_value))
        except ValueError as e:
            return f"Błąd: {e}", 400

        return redirect(url_for("movies"))
