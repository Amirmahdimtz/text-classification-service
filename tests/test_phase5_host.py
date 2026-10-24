"""Phase 5 contract-independent HTTP and fail-closed runtime regressions.

All failure injection is TEST-ONLY; no classification API or model is exposed.
"""
from uuid import UUID

import httpx
import pytest
from fastapi.testclient import TestClient

import src.infrastructure.context.sql_db.psql_dbcontext as db_module
from src.host.app import create_app
from src.host.observability import request_id_var
from src.infrastructure.text_classifier_provider import (
    InferenceUnavailableError,
    TextClassifierProvider,
)


class TestEngine:
    def __init__(self):
        self.disposed = False

    async def dispose(self):
        self.disposed = True


@pytest.mark.asyncio
async def test_existing_http_contract_and_unapproved_routes_remain_closed():
    app = create_app()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        live = await client.get("/health/live")
        ready = await client.get("/health/ready")
        unapproved = await client.post("/api/v1/text_classification/classify", json={"text": "synthetic"})
        review = await client.get("/api/v1/review")
        schema = await client.get("/openapi.json")

    assert live.status_code == 200 and live.json() == {"status": "alive"}
    assert ready.status_code == 503 and ready.json() == {"status": "not_ready"}
    assert unapproved.status_code == review.status_code == schema.status_code == 404
    for response in (live, ready, unapproved, review, schema):
        UUID(response.headers["X-Request-ID"])
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["Referrer-Policy"] == "no-referrer"
        assert response.headers["Cache-Control"] == "no-store"
    assert not hasattr(app.state, "model")
    assert not hasattr(app.state, "classifier")


def test_readiness_failures_and_recovery_are_503_not_500(monkeypatch):
    engine = TestEngine()
    monkeypatch.setattr(db_module, "create_async_engine", lambda *a, **kw: engine)
    observations = iter((True, False, OSError("PRIVATE_DB_HOST"), True))

    async def ping(_self):
        state = next(observations)
        if isinstance(state, Exception):
            raise state
        return state

    monkeypatch.setattr(db_module.PsqlDbContext, "ping_async", ping)
    with TestClient(create_app()) as client:
        lost = client.get("/health/ready")
        raised = client.get("/health/ready")
        restored = client.get("/health/ready")
        assert [lost.status_code, raised.status_code, restored.status_code] == [503, 503, 200]
        assert lost.json() == raised.json() == {"status": "not_ready"}
        assert restored.json() == {"status": "ready"}
        assert "PRIVATE_DB_HOST" not in raised.text
        assert client.get("/health/live").status_code == 200
    assert engine.disposed


@pytest.mark.asyncio
async def test_unhandled_error_redacted_and_request_context_restored():
    app = create_app()

    @app.get("/test-only-unhandled-error")
    async def test_only_failure():
        raise RuntimeError("CONFIDENTIAL_REPORT_TEXT password=SECRET")

    outer = request_id_var.set("outer-test-context")
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/test-only-unhandled-error")
        assert response.status_code == 500
        assert response.json()["error"]["code"] == "INTERNAL_ERROR"
        assert response.json()["error"]["request_id"] == response.headers["X-Request-ID"]
        UUID(response.headers["X-Request-ID"])
        assert "CONFIDENTIAL" not in response.text
        assert "SECRET" not in response.text
        assert request_id_var.get() == "outer-test-context"
    finally:
        request_id_var.reset(outer)


@pytest.mark.asyncio
async def test_model_unconfigured_is_never_warmed_or_successful(monkeypatch):
    monkeypatch.delenv("ML_MODEL_RELEASE_DIR", raising=False)
    monkeypatch.delenv("ML_TAXONOMY_VERSION", raising=False)
    provider = TextClassifierProvider(config_reader=object())  # Test-only dependency.
    try:
        with pytest.raises(InferenceUnavailableError, match="release path"):
            await provider.load_async()
        assert provider.is_ready is False
        with pytest.raises(InferenceUnavailableError, match="not ready"):
            await provider.predict_async(["non-sensitive synthetic input"])
    finally:
        await provider.close_async()
