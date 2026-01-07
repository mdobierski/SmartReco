from flask import redirect, render_template, request, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.movie_service import MovieService
from app.services.rating_service import RatingService


class MovieController(BaseController):
    """
    Controller: movie list (pagination, search), details, rating.
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

        page = int(request.args.get("page", 1))
        search = request.args.get("search") or None
        movies_list, total_pages = self.movie_service.search_paginated(
            query=search, page=page, per_page=20
        )
        user_ratings = self.rating_service.get_user_ratings(user_id)

        return render_template(
            "movies.html",
            movies=movies_list,
            user_ratings=user_ratings,
            page=page,
            total_pages=total_pages,
            search=search or "",
        )

    def movie_detail(self, movie_id: int):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        movie = self.movie_service.get_movie(movie_id)
        if not movie:
            return "Not found", 404

        # Get current rating object if exists
        current_rating = self.rating_service.get_user_rating_object(user_id, movie_id)

        # Get navigation context (return URL or default to movies)
        return_to = request.args.get("return_to", url_for("movies"))

        return render_template(
            "movie_detail.html",
            movie=movie,
            current_rating=current_rating,
            return_to=return_to,
        )

    def rate_movie(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        movie_id = request.form.get("movie_id")
        rating_value = request.form.get("rating")
        return_to = request.form.get("return_to")

        if not movie_id or not rating_value:
            return (
                render_template("error.html", error="Missing required parameters"),
                400,
            )

        try:
            self.rating_service.rate_movie(user_id, int(movie_id), int(rating_value))
        except ValueError as e:
            return render_template("error.html", error=str(e)), 400

        # Return to provided URL or default to movies catalog
        return redirect(return_to if return_to else url_for("movies"))
