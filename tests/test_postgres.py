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
