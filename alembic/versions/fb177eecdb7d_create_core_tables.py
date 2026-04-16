"""create core tables

Revision ID: fb177eecdb7d
Revises: 
Create Date: 2026-04-16 22:51:28.609505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb177eecdb7d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="standard"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("overview", sa.Text(), nullable=True),
        sa.Column("genres", sa.String(length=255), nullable=True),
        sa.Column("poster_url", sa.String(length=512), nullable=True),
        sa.Column("release_year", sa.Integer(), nullable=True),
    )

    op.create_table(
        "user_preferences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("genre", sa.String(length=100), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False, server_default="1"),
    )

    op.create_table(
        "watch_history",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("movie_id", sa.Integer(), sa.ForeignKey("movies.id", ondelete="CASCADE")),
        sa.Column("watched_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "movie_vectors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("movie_id", sa.Integer(), sa.ForeignKey("movies.id", ondelete="CASCADE"), unique=True),
        sa.Column("vector_blob", sa.LargeBinary(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("movie_vectors")
    op.drop_table("watch_history")
    op.drop_table("user_preferences")
    op.drop_table("movies")
    op.drop_table("users")
