import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class Config:
    """Konfiguracja aplikacji"""

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATA_DIR, 'smartreco.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

    DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
