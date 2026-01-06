from typing import Optional

from app.entities.preferences import Preferences
from app.repositories.base import IPreferencesRepository


class PreferenceService:
    """
    Serwis odpowiedzialny za preferencje użytkownika.
    - zapis/nadpis (upsert)
    - pobieranie preferencji
    """

    def __init__(self, prefs_repo: IPreferencesRepository):
        self.prefs_repo = prefs_repo

    def save_preferences(
        self,
        user_id: int,
        countries: Optional[list[str]],
        genres: Optional[list[str]],
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> None:
        """
        Zapisuje lub nadpisuje preferencje (1:1 z userem).
        """
        prefs = Preferences(
            user_id=user_id,
            countries=countries,
            genres=genres,
            year_from=year_from,
            year_to=year_to,
        )
        self.prefs_repo.upsert(prefs)

    def get_preferences(self, user_id: int) -> Optional[Preferences]:
        """
        Pobiera preferencje użytkownika (lub None, jeśli brak).
        """
        return self.prefs_repo.get_by_user_id(user_id)
