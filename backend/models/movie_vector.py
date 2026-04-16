from sqlalchemy import Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.core.database import Base


class MovieVector(Base):
    __tablename__ = "movie_vectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    movie_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("movies.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    vector_blob: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    movie: Mapped["Movie"] = relationship("Movie", back_populates="vector")

