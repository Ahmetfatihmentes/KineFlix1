from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    genres: Mapped[str | None] = mapped_column(String(255), nullable=True)
    poster_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    release_year: Mapped[int | None] = mapped_column(Integer, nullable=True)

    watch_history: Mapped[list["WatchHistory"]] = relationship(
        "WatchHistory", back_populates="movie", cascade="all, delete-orphan"
    )
    vector: Mapped["MovieVector | None"] = relationship(
        "MovieVector", back_populates="movie", uselist=False
    )

