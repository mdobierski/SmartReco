from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Inicjalizacja bazy danych dla aplikacji Flask.
    Tworzy wszystkie tabele na podstawie modeli entities.

    """
    with app.app_context():
        db.create_all()
        print("operation successful - database initialized")
