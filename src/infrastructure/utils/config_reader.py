"""Strict, non-secret application configuration from YAML and environment."""
from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import yaml

from src.infrastructure.di.inject import inject


class ConfigurationError(RuntimeError):
    """Invalid or missing deployment configuration (without secret values)."""


@inject
class ConfigReader:
    __di_singleton__ = True

    def __init__(self):
        env = os.environ.get("ENV_TYPE", "development").strip().lower()
        if env not in ("development", "test", "production"):
            raise ConfigurationError("ENV_TYPE must be development, test or production")
        filename = "appsettings.development.yaml" if env == "development" else "appsettings.yaml"
        config_file = Path(__file__).resolve().parents[2] / "host" / "res" / filename
        try:
            settings = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            raise ConfigurationError("Configuration file invalid or unreadable") from exc
        if not isinstance(settings, dict):
            raise ConfigurationError("Configuration root must be a mapping")
        self.env_type = env
        self._settings = settings
        prefix = self.get("api.prefix")
        if not isinstance(prefix, str) or not prefix.startswith("/") or prefix.endswith("/") or "//" in prefix:
            raise ConfigurationError("api.prefix must be an absolute prefix without trailing slash")
        self.api_prefix = prefix
        if self.get("vault.enabled") is not False:
            raise ConfigurationError("Vault backend is not configured; vault.enabled must be false")
        db_url = os.environ.get("DATABASE_URL", "")
        try:
            parts = urlsplit(db_url)
            hostname = parts.hostname
        except ValueError:
            raise ConfigurationError("DATABASE_URL is malformed") from None
        if parts.scheme != "postgresql+asyncpg" or not hostname or not parts.path.strip("/"):
            raise ConfigurationError("DATABASE_URL must be a valid postgresql+asyncpg DSN from environment")
        if env == "production":
            # Refuse TLS without server hostname/certificate verification.
            ssl_modes = parse_qs(parts.query).get("ssl", [])
            if ssl_modes != ["verify-full"]:
                raise ConfigurationError("Production DATABASE_URL requires TLS ssl=verify-full")
        self.database_url = db_url

    def get(self, dotted_key: str):
        current = self._settings
        for part in dotted_key.split("."):
            if not isinstance(current, dict) or part not in current:
                raise ConfigurationError(f"Missing configuration key: {dotted_key}")
            current = current[part]
        return current

    def get_api_prefix(self) -> str:
        return self.api_prefix
