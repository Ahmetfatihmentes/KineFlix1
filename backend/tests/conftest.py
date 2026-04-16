import pathlib
import sys
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.core.database import Base, get_db
from backend.main import create_app
from backend.models.movie import Movie


TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    session.add_all(
        [
            Movie(
                id=1,
                title="Interstellar",
                overview="Space travel wormhole future science family survival",
                genres="Sci-Fi Drama Adventure",
                release_year=2014,
            ),
            Movie(
                id=2,
                title="The Martian",
                overview="Astronaut survives alone on Mars with science and humor",
                genres="Sci-Fi Adventure",
                release_year=2015,
            ),
            Movie(
                id=3,
                title="Inception",
                overview="Dream layers espionage mind-bending heist thriller",
                genres="Sci-Fi Thriller",
                release_year=2010,
            ),
            Movie(
                id=4,
                title="Gravity",
                overview="Two astronauts struggle to survive in space after disaster",
                genres="Sci-Fi Drama",
                release_year=2013,
            ),
        ]
    )
    session.commit()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
