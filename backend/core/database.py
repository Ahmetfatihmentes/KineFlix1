from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from backend.core.config import get_settings


class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    """


settings = get_settings()

_db_url = str(settings.DATABASE_URL)
_connect_args = (
    {"check_same_thread": False} if _db_url.startswith("sqlite") else {}
)
engine = create_engine(
    _db_url,
    echo=settings.DEBUG,
    connect_args=_connect_args,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    if _db_url.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

