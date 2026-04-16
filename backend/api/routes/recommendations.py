from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.schemas.movie import MovieRead
from backend.services import movie_service


router = APIRouter()


@router.get("/{movie_id}/recommendations", response_model=list[MovieRead])
def get_recommendations(
    movie_id: int,
    db: Session = Depends(get_db),
) -> list[MovieRead]:
    """
    Get recommended movies for a given movie id.
    Uses mock TF-IDF + Cosine Similarity implementation in ai_engine.
    """
    recommendations = movie_service.get_recommendations_for_movie(
        db=db, movie_id=movie_id
    )
    if recommendations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )
    return recommendations

