import pytest

from src.infrastructure.utils.config_reader import ConfigReader, ConfigurationError


def test_config_validates_prefix_and_environment():
    config = ConfigReader()
    assert config.get_api_prefix() == "/api/v1"
    assert config.get("vault.enabled") is False


@pytest.mark.parametrize("key,value", [
    ("ENV_TYPE", "unknown"),
    ("DATABASE_URL", ""),
    ("DATABASE_URL", "sqlite:///test.db"),
    ("DATABASE_URL", "postgresql+asyncpg://localhost"),
])
def test_invalid_config_fails_closed(monkeypatch, key, value):
    monkeypatch.setenv(key, value)
    with pytest.raises(ConfigurationError):
        ConfigReader()


def test_production_requires_tls(monkeypatch):
    monkeypatch.setenv("ENV_TYPE", "production")
    with pytest.raises(ConfigurationError, match="TLS"):
        ConfigReader()


def test_production_refuses_unverified_tls(monkeypatch):
    monkeypatch.setenv("ENV_TYPE", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://service@example.test/prod?ssl=require")
    with pytest.raises(ConfigurationError, match="verify-full"):
        ConfigReader()


def test_production_accepts_verified_tls_mode(monkeypatch):
    monkeypatch.setenv("ENV_TYPE", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://service@example.test/prod?ssl=verify-full")
    assert ConfigReader().env_type == "production"


def test_malformed_ipv6_dsn_is_sanitized(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://[broken-host/prod")
    with pytest.raises(ConfigurationError, match="malformed"):
        ConfigReader()
