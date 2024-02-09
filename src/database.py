from typing import Any

from sqlalchemy import (Column, CursorResult, DateTime, ForeignKey,
                        Identity, Insert, Integer, LargeBinary, MetaData,
                        Select, String, Table, Update, func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


engine = create_async_engine(str(settings.POSTGRESQL_URL))
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

users = Table(
    "users",
    metadata,
    Column("id", Integer, Identity(), primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("password", LargeBinary, nullable=False),
    Column("referral", String(12), ForeignKey("referral_codes.code")),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
    Column("updated_at", DateTime, onupdate=func.now()),
)

referral_codes = Table(
    "referral_codes",
    metadata,
    Column("code", String(12), primary_key=True),
    Column("expiration", DateTime, nullable=False),
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