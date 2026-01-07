from collections import Counter
from typing import Dict, List, Optional, Tuple

from app.entities.movie import Movie
from app.entities.preferences import Preferences
from app.entities.rating import Rating
from app.repositories.base import (
    IMovieRepository,
    IPreferencesRepository,
    IRatingRepository,
)
from app.utils.pagination_helper import paginate, pick_page_size


class RecommendationService:
    def __init__(
        self,
        movie_repo: IMovieRepository,
        prefs_repo: IPreferencesRepository,
        rating_repo: IRatingRepository,
    ) -> None:
        self.movie_repo = movie_repo
        self.prefs_repo = prefs_repo
        self.rating_repo = rating_repo

    # ---------- Shared helpers ----------
    @staticmethod
    def _preference_match_percent(
        movie: Movie,
        countries: Optional[List[str]],
        genres: Optional[List[str]],
        year_from: Optional[int],
        year_to: Optional[int],
    ) -> float:
        genre_w = 0.4
        country_w = 0.3
        year_w = 0.2
        bonus_w = 0.1

        genre_score = 1.0 if genres and movie.genre and movie.genre in genres else 0.0
        country_score = (
            1.0 if countries and movie.country and movie.country in countries else 0.0
        )
        year_score = 0.0
        if movie.year is not None:
            if year_from is not None and movie.year < year_from:
                year_score = 0.0
            elif year_to is not None and movie.year > year_to:
                year_score = 0.0
            else:
                year_score = 1.0
        bonus_score = 1.0 if (movie.vote_average or 0) >= 7.0 else 0.0

        total = (
            genre_score * genre_w
            + country_score * country_w
            + year_score * year_w
            + bonus_score * bonus_w
        )
        return total * 100.0

    @staticmethod
    def _cutoff_for_user_likes(user_ratings: List[Rating]) -> Optional[int]:
        if not user_ratings:
            return None
        r_max = max(r.rating for r in user_ratings)
        cutoff = max(6, r_max - 2)
        return cutoff

    # ---------- Criteria-based filtering ----------
    def recommend_with_filters(
        self,
        countries: Optional[List[str]] = None,
        genres: Optional[List[str]] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        page: int = 1,
    ) -> Tuple[List[Movie], int]:
        """
        Filter movies by criteria using repository.
        No scoring - movies either match or don't.
        """
        movies = self.movie_repo.filter_movies(
            countries=countries or [],
            genres=genres or [],
            year_from=year_from,
            year_to=year_to,
        )

        per_page = pick_page_size(len(movies))
        page_items, total_pages = paginate(movies, page, per_page)
        return page_items, total_pages

    # ---------- Personal hybrid ----------
    def recommend_for_user(
        self, user_id: int, page: int = 1
    ) -> Tuple[List[Movie], int, List[float]]:
        prefs = self.prefs_repo.get_by_user_id(user_id)
        countries = prefs.countries if prefs else None
        genres = prefs.genres if prefs else None
        year_from = prefs.year_from if prefs else None
        year_to = prefs.year_to if prefs else None

        user_ratings = self.rating_repo.get_user_ratings(user_id)
        cutoff = self._cutoff_for_user_likes(user_ratings)
        liked_ids = {r.movie_id for r in user_ratings if cutoff and r.rating >= cutoff}

        # Get all rated movie IDs to exclude from recommendations
        rated_movie_ids = {r.movie_id for r in user_ratings}

        # global avg (C) and m
        all_movies = self.movie_repo.get_all()
        global_avg = (
            sum(m.vote_average or 0 for m in all_movies) / len(all_movies)
            if all_movies
            else 0
        )
        m_min = 50

        # neighbor co-occurrence (light)
        neighbor_counter: Counter[int] = Counter()
        if liked_ids:
            for mid in liked_ids:
                others = self.rating_repo.get_ratings_for_movie(mid)
                for r in others:
                    if r.user_id != user_id and cutoff and r.rating >= cutoff:
                        neighbor_counter[r.movie_id] += 1
        max_co = max(neighbor_counter.values()) if neighbor_counter else 0

        def neighbor_norm(movie_id: int) -> float:
            if max_co == 0:
                return 0.0
            return min(1.0, neighbor_counter.get(movie_id, 0) / max_co)

        def rating_lift(m: Movie) -> float:
            if not liked_ids:
                return 1.0
            liked_ratings = [r for r in user_ratings if r.rating >= (cutoff or 0)]
            if not liked_ratings:
                return 1.0
            user_avg = sum(r.rating for r in liked_ratings) / len(liked_ratings)
            bonus = max(0.0, ((m.vote_average or 0) - user_avg) / 3 * 0.15)
            return 1.0 + min(bonus, 0.3)

        scored: List[Tuple[Movie, float, float]] = []
        for m in all_movies:
            # Skip movies that user has already rated
            if m.id in rated_movie_ids:
                continue

            pm = self._preference_match_percent(
                m, countries, genres, year_from, year_to
            )
            if pm < 20.0:
                continue
            pm_norm = pm / 100.0
            R = m.vote_average or 0
            v = m.vote_count or 0
            pop_score = (v / (v + m_min)) * R + (m_min / (v + m_min)) * global_avg
            pop_norm = pop_score / 10.0
            neigh = neighbor_norm(m.id or -1)
            lift = rating_lift(m)
            pop_weight = 0.25
            neigh_weight = 0.15
            score = pm_norm * (1 + pop_weight * pop_norm + neigh_weight * neigh) * lift
            scored.append((m, score, pm))
        scored.sort(key=lambda x: x[1], reverse=True)

        per_page = pick_page_size(len(scored))
        page_items, total_pages = paginate([s[0] for s in scored], page, per_page)
        percents = [s[2] for s in scored][
            (page - 1) * per_page : (page - 1) * per_page + len(page_items)
        ]
        return page_items, total_pages, percents
