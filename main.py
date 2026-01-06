from flask import Flask

from app.controllers.auth_controller import AuthController
from app.controllers.home_controller import HomeController
from app.controllers.movie_controller import MovieController
from app.controllers.preference_controller import PreferenceController
from app.controllers.recommendation_controller import RecommendationController
from app.database import db, init_db
from app.repositories.movie_repository import SqlMovieRepository
from app.repositories.preferences_repository import SqlPreferencesRepository
from app.repositories.rating_repository import SqlRatingRepository
from app.repositories.user_repository import SqlUserRepository
from app.services.auth_service import AuthService
from app.services.movie_service import MovieService
from app.services.preference_service import PreferenceService
from app.services.rating_service import RatingService
from app.services.recommendation_service import RecommendationService
from app.utils.password_hasher import PasswordHasherService
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    # WARSTWA REPOZYTORIÓW (Data Access)
    user_repo = SqlUserRepository()
    movie_repo = SqlMovieRepository()
    rating_repo = SqlRatingRepository()
    prefs_repo = SqlPreferencesRepository()

    # WARSTWA SERWISÓW (Business Logic)
    password_hasher = PasswordHasherService()
    auth_service = AuthService(user_repo, password_hasher)
    movie_service = MovieService(movie_repo)
    rating_service = RatingService(rating_repo)
    preference_service = PreferenceService(prefs_repo)
    recommendation_service = RecommendationService(movie_repo, prefs_repo)

    # WARSTWA KONTROLERÓW (HTTP Handling)
    home_controller = HomeController(user_repo, preference_service)
    auth_controller = AuthController(user_repo, auth_service)
    movie_controller = MovieController(user_repo, movie_service, rating_service)
    preference_controller = PreferenceController(
        user_repo, movie_service, preference_service
    )
    recommendation_controller = RecommendationController(
        user_repo, movie_service, preference_service, recommendation_service
    )

    #  ROUTING (mapowanie URL → metody kontrolerów)

    app.add_url_rule("/", "index", home_controller.index, methods=["GET"])

    app.add_url_rule("/login", "login", auth_controller.login_get, methods=["GET"])
    app.add_url_rule(
        "/login", "login_post", auth_controller.login_post, methods=["POST"]
    )
    app.add_url_rule(
        "/register", "register", auth_controller.register_get, methods=["GET"]
    )
    app.add_url_rule(
        "/register", "register_post", auth_controller.register_post, methods=["POST"]
    )
    app.add_url_rule("/logout", "logout", auth_controller.logout, methods=["GET"])

    app.add_url_rule("/movies", "movies", movie_controller.list_movies, methods=["GET"])
    app.add_url_rule("/rate", "rate", movie_controller.rate_movie, methods=["POST"])

    app.add_url_rule(
        "/preferences", "preferences", preference_controller.show_form, methods=["GET"]
    )
    app.add_url_rule(
        "/preferences",
        "preferences_post",
        preference_controller.save_preferences,
        methods=["POST"],
    )

    app.add_url_rule(
        "/criteria-recommendation",
        "criteria_recommendation",
        recommendation_controller.criteria_form,
        methods=["GET"],
    )
    app.add_url_rule(
        "/criteria-recommendation",
        "criteria_recommendation_post",
        recommendation_controller.criteria_recommend,
        methods=["POST"],
    )
    app.add_url_rule(
        "/personal-recommendation",
        "personal_recommendation",
        recommendation_controller.personal_recommend,
        methods=["GET"],
    )

    return app


if __name__ == "__main__":
    app = create_app()
    init_db(app)
    app.run(debug=True)
