from pydantic import BaseModel, ConfigDict


class MovieRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    overview: str | None = None
    genres: str | None = None
    poster_url: str | None = None
    release_year: int | None = None
