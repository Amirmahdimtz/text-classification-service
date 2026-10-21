"""Vault safety gate; no fake remote secret-store integration."""
from src.infrastructure.di.inject import inject
from src.infrastructure.utils.config_reader import ConfigReader


@inject
class VaultService:
    __di_singleton__ = True

    def __init__(self, config_reader: ConfigReader):
        if config_reader.get("vault.enabled") is not False:
            raise RuntimeError("An approved vault integration is required before enabling Vault")
