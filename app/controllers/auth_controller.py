from typing import Optional

from flask import redirect, render_template, request, session, url_for

from app.controllers.base_controller import BaseController
from app.repositories.base import IUserRepository
from app.services.auth_service import AuthService


class AuthController(BaseController):
    """
    Kontroler odpowiedzialny za autentykację użytkowników.
    Odpowiedzialność: login, register, logout (warstwa HTTP).
    """

    def __init__(self, user_repo: IUserRepository, auth_service: AuthService):
        super().__init__(user_repo)
        self.auth_service = auth_service

    def login_get(self):
        return render_template("login.html")

    def login_post(self):
        email = request.form["email"]
        password = request.form["password"]

        user = self.auth_service.login(email, password)
        if user:
            session["user_email"] = user.email
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Wrong email or password")

    def register_get(self):
        return render_template("register.html")

    def register_post(self):
        email = request.form["email"]
        password = request.form["password"]

        user = self.auth_service.register(email, password)
        if not user:
            return render_template("register.html", error="User already exists")

        session["user_email"] = user.email
        return redirect(url_for("preferences"))

    def logout(self):
        session.pop("user_email", None)
        return redirect(url_for("login"))
