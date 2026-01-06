from typing import Optional

from app.database import db
from app.entities.preferences import Preferences
from app.repositories.base import IPreferencesRepository


class SqlPreferencesRepository(IPreferencesRepository):

    def upsert(self, prefs: Preferences) -> None:
        existing = Preferences.query.filter_by(user_id=prefs.user_id).first()
        if existing:
            existing.countries = prefs.countries
            existing.genres = prefs.genres
            existing.year_from = prefs.year_from
            existing.year_to = prefs.year_to
        else:
            db.session.add(prefs)
        db.session.commit()

    def get_by_user_id(self, user_id: int) -> Optional[Preferences]:
        return Preferences.query.filter_by(user_id=user_id).first()
