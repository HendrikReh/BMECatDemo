"""Database connection and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.db.models import Base

# Async engine for FastAPI
async_engine = create_async_engine(settings.postgres_url, echo=False)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

# Sync engine for bulk imports
sync_engine = create_engine(settings.postgres_url_sync, echo=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to get async database session."""
    async with async_session_maker() as session:
        yield session


async def init_db() -> None:
    """Create all tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def init_db_sync() -> None:
    """Create all tables (sync version for scripts)."""
    Base.metadata.create_all(sync_engine)
