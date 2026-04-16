from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.ai_engine.recommender import MockRecommender
from backend.models.movie import Movie


recommender = MockRecommender()


def search_movies(db: Session, query: str) -> list[Movie]:
    statement = select(Movie).where(
        or_(
            Movie.title.ilike(f"%{query}%"),
            Movie.overview.ilike(f"%{query}%"),
        )
    )
    return list(db.scalars(statement).all())


def get_recommendations_for_movie(db: Session, movie_id: int) -> list[Movie] | None:
    movie = db.get(Movie, movie_id)
    if movie is None:
        return None

    recommended_ids = [item.movie_id for item in recommender.recommend(movie_id)]
    if not recommended_ids:
        return []

    statement = select(Movie).where(Movie.id.in_(recommended_ids))
    movies = list(db.scalars(statement).all())
    movie_by_id = {movie_item.id: movie_item for movie_item in movies}
    return [movie_by_id[movie_id] for movie_id in recommended_ids if movie_id in movie_by_id]
