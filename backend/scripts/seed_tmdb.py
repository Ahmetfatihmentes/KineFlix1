from __future__ import annotations

import argparse
import logging

import httpx
from sqlalchemy import select

from backend.core.config import get_settings
from backend.core.database import SessionLocal
from backend.models.movie import Movie


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

TMDB_BASE_URL = "https://api.themoviedb.org/3"


def _auth_headers(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }


def _get_genre_map(client: httpx.Client, token: str) -> dict[int, str]:
    response = client.get(
        f"{TMDB_BASE_URL}/genre/movie/list",
        headers=_auth_headers(token),
        params={"language": "en-US"},
        timeout=20.0,
    )
    response.raise_for_status()
    data = response.json()
    return {genre["id"]: genre["name"] for genre in data.get("genres", [])}


def _fetch_popular_movies(
    client: httpx.Client, token: str, pages: int
) -> list[dict]:
    movies: list[dict] = []
    for page in range(1, pages + 1):
        response = client.get(
            f"{TMDB_BASE_URL}/movie/popular",
            headers=_auth_headers(token),
            params={"language": "en-US", "page": page},
            timeout=20.0,
        )
        response.raise_for_status()
        payload = response.json()
        batch = payload.get("results", [])
        logger.info("Fetched %s popular movies from page %s", len(batch), page)
        movies.extend(batch)
    return movies


def seed_tmdb_popular_movies(pages: int = 1) -> int:
    settings = get_settings()
    token = settings.TMDB_READ_ACCESS_TOKEN
    if not token:
        raise RuntimeError("TMDB_READ_ACCESS_TOKEN is missing in environment/.env")

    inserted_or_updated = 0
    with httpx.Client() as client:
        genre_map = _get_genre_map(client, token)
        popular_movies = _fetch_popular_movies(client, token, pages)

    with SessionLocal() as db:
        for item in popular_movies:
            tmdb_movie_id = item.get("id")
            title = item.get("title")
            if not tmdb_movie_id or not title:
                continue

            overview = item.get("overview")
            release_date = item.get("release_date") or ""
            release_year = (
                int(release_date[:4]) if len(release_date) >= 4 and release_date[:4].isdigit() else None
            )
            poster_path = item.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            genre_ids = item.get("genre_ids", [])
            genres = ", ".join(
                genre_map[genre_id] for genre_id in genre_ids if genre_id in genre_map
            ) or None

            existing = db.scalar(select(Movie).where(Movie.id == int(tmdb_movie_id)))
            if existing:
                existing.title = title
                existing.overview = overview
                existing.genres = genres
                existing.poster_url = poster_url
                existing.release_year = release_year
            else:
                db.add(
                    Movie(
                        id=int(tmdb_movie_id),
                        title=title,
                        overview=overview,
                        genres=genres,
                        poster_url=poster_url,
                        release_year=release_year,
                    )
                )
            inserted_or_updated += 1

        db.commit()

    logger.info("Seed completed. Inserted/updated: %s", inserted_or_updated)
    return inserted_or_updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed popular movies from TMDB.")
    parser.add_argument("--pages", type=int, default=1, help="How many TMDB pages to fetch")
    args = parser.parse_args()

    if args.pages < 1:
        raise ValueError("--pages must be >= 1")

    seed_tmdb_popular_movies(pages=args.pages)


if __name__ == "__main__":
    main()
