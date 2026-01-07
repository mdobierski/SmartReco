from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Initialize database for Flask application.
    Creates all tables based on entity models.
    """
    with app.app_context():
        db.create_all()
        print("operation successful - database initialized")
