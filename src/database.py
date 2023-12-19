from typing import Any

from sqlalchemy import (
    Boolean,
    Column,
    CursorResult,
    DateTime,
    ForeignKey,
    Identity,
    Insert,
    Integer,
    Float,
    LargeBinary,
    MetaData,
    Select,
    String,
    Table,
    Update,
    func,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL)

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

auth_user = Table(
    "users",
    metadata,
    Column("user_id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False),
    Column("nickname", String),
    Column("password", LargeBinary, nullable=False),
    Column("is_admin", Boolean, server_default="false", nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

refresh_tokens = Table(
    "auth_refresh_token",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("user_id", ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False),
    Column("refresh_token", String, nullable=False),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

anime = Table(
    "animes",
    metadata,
    Column("anime_id", Integer, Identity(), primary_key=True),
    Column("mal_anime_id", Integer),
    Column("title", String, nullable=False),
    Column("synopsis", String),
    Column("preview_image_url", String),
    Column("episodes", Integer),
    Column("air_start_date", DateTime),
    Column("air_end_date", DateTime),
    Column("mal_score", Float),
    Column("mal_ranked", Integer),
    Column("mal_popularity", Integer),
    Column("mal_members", Integer),
)

catalog = Table(
    "catalogs",
    metadata,
    Column("catalog_id", Integer, Identity(), primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("is_preview", Boolean),
)

catalog_anime = Table(
    "catalog_animes",
    metadata,
    Column("catalog_anime_id", Integer, Identity(), primary_key=True),
    Column("catalog_id", Integer, nullable=False),
    Column("anime_id", Integer, nullable=False),
)

review = Table(
    "reviews",
    metadata,
    Column("review_id", Integer, Identity(), primary_key=True),
    Column("anime_id", Integer, nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("text", String),
    Column("overall_score", Integer, nullable=False),
    Column("animation_score", Integer),
    Column("sound_score", Integer),
    Column("character_score", Integer),
    Column("enjoyment_score", Integer),
)


async def fetch_one(select_query: Select | Insert | Update) -> dict[str, Any] | None:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.first()._asdict() if cursor.rowcount > 0 else None


async def fetch_all(select_query: Select | Insert | Update) -> list[dict[str, Any]]:
    async with engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [r._asdict() for r in cursor.all()]


async def execute(select_query: Insert | Update) -> None:
    async with engine.begin() as conn:
        await conn.execute(select_query)
