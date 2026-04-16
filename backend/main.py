from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.error_handlers import register_exception_handlers
from backend.api.routes import auth, movies, recommendations
from backend.core.bootstrap import initialize_database
from backend.core import logging_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


def create_app() -> FastAPI:
    """
    Application factory to create FastAPI app with routes and middleware.
    """
    logging_config.configure_logging()

    app = FastAPI(title="KineFlix Backend", version="0.1.0", lifespan=lifespan)

    # Register global exception handlers
    register_exception_handlers(app)

    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(movies.router, prefix="/movies", tags=["movies"])
    app.include_router(
        recommendations.router, prefix="/movies", tags=["recommendations"]
    )

    return app


app = create_app()

