from typing import List, Optional

from app.entities.preferences import Preferences
from app.repositories.base import IPreferencesRepository


class PreferenceService:
    """
    Service responsible for user preferences.
    - save/overwrite (upsert)
    - retrieve preferences
    """

    def __init__(self, prefs_repo: IPreferencesRepository):
        self.prefs_repo = prefs_repo

    def save_preferences(
        self,
        user_id: int,
        countries: Optional[List[str]],
        genres: Optional[List[str]],
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> None:
        """
        Save or overwrite preferences (1:1 with user).
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
        Retrieve user preferences (or None if not set).
        """
        return self.prefs_repo.get_by_user_id(user_id)
