"""Never use real confidential data or live service credentials in test fixtures."""
import os

import pytest

from src.infrastructure.di.bootstrap import shutdown_di


@pytest.fixture(autouse=True)
def isolated_di(monkeypatch):
    shutdown_di()
    monkeypatch.setenv("ENV_TYPE", "test")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://phase2@127.0.0.1:5432/phase2_test")
    yield
    shutdown_di()
