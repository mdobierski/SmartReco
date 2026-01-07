import time
from typing import Dict, List, Optional

import requests


class TMDbClient:
    """
    Client for TMDb API communication.
    Handles fetching movies and their details.
    """

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:

        if params is None:
            params = {}  # all calls use this separate dictionary
        params["api_key"] = self.api_key
        params["language"] = "en-US"

        url = f"{self.BASE_URL}{endpoint}"
        # API rate limit: 4 requests per second
        time.sleep(0.25)

        response = self.session.get(url, params=params)
        response.raise_for_status()  # Raises exception on HTTP error

        return response.json()

    def get_top_rated_movies(self, page: int = 1) -> Dict:
        return self._make_request("/movie/top_rated", {"page": page})

    def get_movie_details(self, movie_id: int) -> Dict:
        return self._make_request(
            f"/movie/{movie_id}", {"append_to_response": "credits"}
        )

    def extract_director(self, movie_details: Dict) -> Optional[str]:
        credits = movie_details.get("credits", {})
        crew = credits.get("crew", [])
        for person in crew:
            if person.get("job") == "Director":
                return person.get("name")
        return None

    def extract_country(self, movie_details: Dict) -> Optional[str]:
        countries = movie_details.get("production_countries", [])
        if not countries:
            return None

        # Priorytet: USA i UK jako główni producenci
        country_names = [c.get("name") for c in countries]

        if "United States of America" in country_names:
            return "United States of America"
        if "United Kingdom" in country_names:
            return "United Kingdom"

        # W przeciwnym razie pierwszy z listy
        return countries[0].get("name")
