"""Lifespan control-flow tests only: fake engine is test-scoped, not DB evidence."""
import pytest
from fastapi.testclient import TestClient

import src.infrastructure.context.sql_db.psql_dbcontext as db_module
from src.host.app import create_app


class FakeEngine:
    def __init__(self):
        self.disposed = False

    async def dispose(self):
        self.disposed = True


@pytest.mark.parametrize("available", [True, False])
def test_lifespan_database_gate_and_cleanup(monkeypatch, available):
    engine = FakeEngine()
    monkeypatch.setattr(db_module, "create_async_engine", lambda *args, **kwargs: engine)

    async def ping(self):
        return available

    monkeypatch.setattr(db_module.PsqlDbContext, "ping_async", ping)
    app = create_app()
    if available:
        with TestClient(app) as client:
            response = client.get("/health/ready")
            assert response.status_code == 200
            assert response.json() == {"status": "ready"}
    else:
        with pytest.raises(RuntimeError, match="Database is not ready"):
            with TestClient(app):
                pass
    assert engine.disposed
