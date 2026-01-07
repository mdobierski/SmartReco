from flask import redirect, render_template, request, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.rating_service import RatingService


class RatingController(BaseController):
    def __init__(self, rating_service: RatingService, user_repo: IUserRepository):
        super().__init__(user_repo)
        self.rating_service = rating_service

    def my_reviews(self):
        """Display all user's ratings with movie details, with search."""
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        search = request.args.get("search", "", type=str)
        ratings_with_movies = self.rating_service.get_ratings_with_movies(
            user_id, search
        )

        # Transform to list of dicts for easier template access
        reviews = []
        for rating, movie in ratings_with_movies:
            reviews.append({"rating": rating, "movie": movie})

        return render_template("reviews.html", reviews=reviews, search=search)

    def delete_review(self):
        """Delete user's rating and stay on current page or redirect back to source."""
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect

        user_id = self.get_current_user_id()

        movie_id = request.form.get("movie_id", type=int)
        return_to = request.form.get("return_to", url_for("my_reviews"))
        from_detail = request.form.get("from_detail")

        if movie_id:
            self.rating_service.delete_rating(user_id, movie_id)

        # If deleting from movie_detail page, stay there with return_to preserved
        if from_detail:
            return redirect(
                url_for("movie_detail", movie_id=movie_id, return_to=return_to)
            )

        # Otherwise redirect directly to source (e.g., movies with page/search, my_reviews)
        return redirect(return_to)
