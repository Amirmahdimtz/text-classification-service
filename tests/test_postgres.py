"""Opt-in integration against an isolated test database only."""
import os

import pytest
from sqlalchemy import text

from src.infrastructure.context.sql_db.psql_dbcontext import PsqlDbContext
from src.infrastructure.di.bootstrap import bootstrap_di, resolve


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_postgres_sessions_transactions_and_rollback(monkeypatch):
    url = os.getenv("TEST_DATABASE_URL", "")
    if not url:
        pytest.skip("TEST_DATABASE_URL not configured; actual PostgreSQL verification BLOCKED")
    assert url.startswith("postgresql+asyncpg://") and url.split("?", 1)[0].endswith("_test"), "Only isolated *_test databases are permitted"
    monkeypatch.setenv("DATABASE_URL", url)
    bootstrap_di()
    db = resolve(PsqlDbContext)
    try:
        assert await db.ping_async()
        async with db.transaction() as session:
            assert (await session.execute(text("SELECT 1"))).scalar_one() == 1
        with pytest.raises(ZeroDivisionError):
            async with db.transaction() as session:
                await session.execute(text("CREATE TEMP TABLE phase2_rollback_probe (value INT)"))
                raise ZeroDivisionError("trigger rollback")
        async with db.session() as session:
            # Transactional DDL must not be visible after rollback.
            value = (await session.execute(text("SELECT to_regclass('pg_temp.phase2_rollback_probe')"))).scalar_one()
            assert value is None
    finally:
        await db.close_async()


@pytest.mark.postgres
def test_real_fastapi_lifespan_with_postgresql(monkeypatch):
    """Only live database integration: not a unit-test double."""
    from fastapi.testclient import TestClient
    from src.host.app import create_app

    url = os.getenv("TEST_DATABASE_URL", "")
    if not url:
        pytest.skip("TEST_DATABASE_URL not configured")
    assert url.startswith("postgresql+asyncpg://") and url.split("?", 1)[0].endswith("_test")
    monkeypatch.setenv("DATABASE_URL", url)
    with TestClient(create_app()) as client:
        assert client.get("/health/live").status_code == 200
        ready = client.get("/health/ready")
        assert ready.status_code == 200 and ready.json() == {"status": "ready"}


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_base_repository_crud_on_postgres(monkeypatch):
    """Use a PostgreSQL TEMPORARY table confined to the test connection."""
    from sqlalchemy import String
    from sqlalchemy.orm import Mapped, mapped_column
    from src.infrastructure.context.sql_db.psql_dbcontext import Base
    from src.infrastructure.repositories.base.base_repository import BaseRepository

    url = os.getenv("TEST_DATABASE_URL", "")
    if not url:
        pytest.skip("TEST_DATABASE_URL not configured")
    assert url.startswith("postgresql+asyncpg://") and url.split("?", 1)[0].endswith("_test")
    monkeypatch.setenv("DATABASE_URL", url)

    class Probe(Base):
        __tablename__ = "phase2_crud_probe"
        __table_args__ = {"prefixes": ["TEMPORARY"]}
        id: Mapped[int] = mapped_column(primary_key=True)
        label: Mapped[str] = mapped_column(String(60), nullable=False)

    bootstrap_di()
    db = resolve(PsqlDbContext)
    try:
        async with db._engine.begin() as connection:
            await connection.run_sync(Probe.__table__.create)
        repo = BaseRepository(db, Probe)
        inserted = await repo.insert_async(Probe(label="before"))
        assert inserted.id is not None
        assert (await repo.get_by_id_async(inserted.id)).label == "before"
        assert len(await repo.get_all_async()) == 1
        inserted.label = "after"
        assert (await repo.update_async(inserted)).label == "after"
        assert await repo.delete_async(inserted.id) is True
        assert await repo.delete_async(inserted.id) is False
        assert await repo.get_by_id_async(inserted.id) is None
    finally:
        await db.close_async()


@pytest.mark.postgres
@pytest.mark.asyncio
async def test_phase5_isolated_postgres_connection_failure_and_recovery():
    """A refused localhost test connection must not be interpreted as ready.

    The healthy branch connects to the real isolated test DB. No server is stopped,
    no production data is touched, and no migration or schema mutation occurs.
    """
    from types import SimpleNamespace
    from sqlalchemy.engine import make_url

    url = os.getenv("TEST_DATABASE_URL", "")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not configured")
    assert url.startswith("postgresql+asyncpg://") and url.split("?", 1)[0].endswith("_test")

    isolated_url = make_url(url)
    refused = isolated_url.set(host="127.0.0.1", port=1)
    unavailable = PsqlDbContext(
        config_reader=SimpleNamespace(database_url=refused.render_as_string(hide_password=False)),
        vault_service=object(),  # Explicit test dependency, never a runtime provider.
    )
    try:
        assert await unavailable.ping_async() is False
    finally:
        await unavailable.close_async()

    available = PsqlDbContext(
        config_reader=SimpleNamespace(database_url=url),
        vault_service=object(),
    )
    try:
        assert await available.ping_async() is True
    finally:
        await available.close_async()
