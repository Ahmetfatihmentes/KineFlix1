from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.database import DATABASE_URL as _DEFAULT_SQLITE_URL


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    DATABASE_URL: str = _DEFAULT_SQLITE_URL
    DEBUG: bool = True
    TMDB_READ_ACCESS_TOKEN: str | None = None
    TMDB_API_KEY: str | None = None
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()

