from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.schemas.movie import MovieRead
from backend.services import movie_service


router = APIRouter()


@router.get("/search", response_model=list[MovieRead])
def search_movies(
    q: str = Query(..., alias="query", min_length=1),
    db: Session = Depends(get_db),
) -> list[MovieRead]:
    """
    Search movies by title or overview.
    """
    return movie_service.search_movies(db=db, query=q)

