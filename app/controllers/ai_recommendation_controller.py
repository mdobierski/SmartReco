from flask import render_template

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository


class AiRecommendationController(BaseController):
    """
    Kontroler rekomendacji AI.
    Odpowiedzialność: wyświetlanie strony Coming Soon.
    """

    def __init__(self, user_repo: IUserRepository):
        super().__init__(user_repo)

    def coming_soon(self):
        auth_redirect = self.require_auth()
        if auth_redirect:
            return auth_redirect
        return render_template("ai_coming_soon.html")
