from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.schemas.user import UserCreate, UserRead
from backend.services import auth_service


router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """
    User registration endpoint.
    """
    return auth_service.register_user(db=db, user_in=user_in)

