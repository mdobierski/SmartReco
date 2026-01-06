"""
Importer TMDb - pobiera top-rated filmy z The Movie Database API.
Enrich szczegółami (runtime, director, country) i zapisuje do bazy.
"""

import os
import sys

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import main
from app.entities.movie import Movie
from app.repositories.movie_repository import SqlMovieRepository
from app.utils.tmdb_client import TMDbClient

load_dotenv()


def import_tmdb_movies(total_pages: int = 500):
    api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        raise ValueError("TMDB_API_KEY nie ustawiony w .env")

    print(f"Rozpoczynam import {total_pages} stron filmów z TMDb...")
    print("Rate limit: 4 req/s (0.25s/request)")
    print("Szacowany czas: ~40-60 minut\n")

    client = TMDbClient(api_key)
    repo = SqlMovieRepository()

    imported_count = 0

    for page in range(1, total_pages + 1):
        print(f"[{page}/{total_pages}] Pobieranie strony...")

        try:
            response = client.get_top_rated_movies(page)
        except Exception as e:
            print(f"Błąd pobierania strony {page}: {e}")
            continue

        results = response.get("results", [])
        if not results:
            print("Brak wyników, kończę import.")
            break

        movies_batch = []
        skipped_count = 0

        for item in results:
            tmdb_id = item.get("id")
            if not tmdb_id:
                continue

            existing = repo.get_by_tmdb_id(tmdb_id)
            if existing:
                skipped_count += 1
                continue

            try:
                details = client.get_movie_details(tmdb_id)
            except Exception as e:
                print(f"Błąd szczegółów dla tmdb_id={tmdb_id}: {e}")
                continue

            title = details.get("title", "")
            original_title = details.get("original_title")

            year = None
            release_date = details.get("release_date")
            if release_date and len(release_date) >= 4:
                year = int(release_date[:4])

            runtime = details.get("runtime")
            overview = details.get("overview")
            poster_path = details.get("poster_path")
            vote_average = details.get("vote_average")
            vote_count = details.get("vote_count")

            genres = details.get("genres", [])
            genre = genres[0].get("name") if genres else None

            director = client.extract_director(details)
            country = client.extract_country(details)

            movie = Movie(
                tmdb_id=tmdb_id,
                title=title,
                original_title=original_title,
                year=year,
                runtime=runtime,
                overview=overview,
                poster_path=poster_path,
                genre=genre,
                country=country,
                director=director,
                vote_average=vote_average,
                vote_count=vote_count,
            )
            movies_batch.append(movie)

        if movies_batch:
            try:
                repo.save_many(movies_batch)
                imported_count += len(movies_batch)
                status = f"Zapisano {len(movies_batch)} filmów"
                if skipped_count > 0:
                    status += f" (pominięto {skipped_count} duplikatów)"
                status += f" (łącznie: {imported_count})"
                print(status)
            except Exception as e:
                print(f"Błąd zapisu: {e}")
                from app.database import db

                db.session.rollback()
        elif skipped_count > 0:
            print(f"  ⏭️ Pominięto {skipped_count} duplikatów")

    print(f"\n{'='*60}")
    print(f"Import zakończony!")
    print(f"Zaimportowano: {imported_count} filmów")
    print(f"{'='*60}")


if __name__ == "__main__":
    flask_app = main.create_app()
    with flask_app.app_context():
        import_tmdb_movies(total_pages=500)
