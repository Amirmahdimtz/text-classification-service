"""Reusable, operation-scoped SQLAlchemy CRUD; not a multi-row unit-of-work."""
from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.context.sql_db.psql_dbcontext import PsqlDbContext

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepository(Generic[T]):
    def __init__(self, db_context: PsqlDbContext, model: type[T]):
        self._db_context = db_context
        self._model = model

    async def insert_async(self, entity: T) -> T:
        async with self._db_context.session() as session:
            async with session.begin():
                session.add(entity)
                await session.flush()
                await session.refresh(entity)
            return entity

    async def insert_and_get_id_async(self, entity: T):
        inserted = await self.insert_async(entity)
        return inserted.id

    async def get_by_id_async(self, entity_id) -> T | None:
        async with self._db_context.session() as session:
            return await session.get(self._model, entity_id)

    async def get_all_async(self) -> list[T]:
        async with self._db_context.session() as session:
            result = await session.scalars(select(self._model))
            return list(result.all())

    async def update_async(self, entity: T) -> T:
        async with self._db_context.session() as session:
            async with session.begin():
                merged = await session.merge(entity)
                await session.flush()
                await session.refresh(merged)
            return merged

    async def delete_async(self, entity_id) -> bool:
        async with self._db_context.session() as session:
            async with session.begin():
                obj = await session.get(self._model, entity_id)
                if obj is None:
                    return False
                await session.delete(obj)
            return True
