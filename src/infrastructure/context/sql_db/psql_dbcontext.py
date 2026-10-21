"""Shared PostgreSQL async engine; per-operation sessions and atomic units."""
from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.context.vault.vault_service import VaultService
from src.infrastructure.di.inject import inject
from src.infrastructure.utils.config_reader import ConfigReader


class Base(DeclarativeBase):
    pass


@inject
class PsqlDbContext:
    __di_singleton__ = True

    def __init__(self, config_reader: ConfigReader, vault_service: VaultService):
        # vault_service participates in validated dependency resolution; never log the DSN.
        self._engine = create_async_engine(
            config_reader.database_url, pool_pre_ping=True, pool_timeout=10,
            connect_args={"timeout": 5},
        )
        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False, autoflush=False,
        )

    def session(self) -> AsyncSession:
        return self._session_factory()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSession]:
        """One bounded transaction for a future approved multi-record write."""
        async with self._session_factory.begin() as session:
            yield session

    async def ping_async(self) -> bool:
        try:
            async with self.session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    async def close_async(self) -> None:
        await self._engine.dispose()
