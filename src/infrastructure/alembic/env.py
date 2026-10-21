"""Migration environment, intentionally empty metadata until schema is approved."""
from __future__ import annotations

import asyncio

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from src.infrastructure.context.sql_db.psql_dbcontext import Base
from src.infrastructure.utils.config_reader import ConfigReader

# Import approved SQLAlchemy models here when a reviewed schema is introduced.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    raise RuntimeError("Offline migration generation with embedded credentials is disabled")


async def run_migrations_online() -> None:
    settings = ConfigReader()
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    try:
        async with engine.connect() as connection:
            def do_run_migrations(sync_connection):
                context.configure(connection=sync_connection, target_metadata=target_metadata, compare_type=True)
                with context.begin_transaction():
                    context.run_migrations()

            await connection.run_sync(do_run_migrations)
    finally:
        await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
