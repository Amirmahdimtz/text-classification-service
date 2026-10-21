"""Fail-fast module and provider discovery by architecture convention."""
from __future__ import annotations

import importlib
import inspect
import pkgutil

from src.infrastructure.di.inject import DependencyError

_EXCLUDED = {"di", "dtos", "models", "scripts", "alembic", "versions", "res", "sso"}
_ROOTS = ("src.infrastructure", "src.core", "src.application")


def discover_providers() -> dict[type, type]:
    providers: dict[type, type] = {}
    for root in _ROOTS:
        package = importlib.import_module(root)
        for module_info in pkgutil.walk_packages(package.__path__, prefix=package.__name__ + "."):
            parts = module_info.name.split(".")
            if any(part in _EXCLUDED for part in parts):
                continue
            try:
                module = importlib.import_module(module_info.name)
            except Exception as exc:
                raise DependencyError(f"Failed to import provider module {module_info.name}") from exc
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ != module.__name__ or not obj.__dict__.get("__di_provider__", False):
                    continue
                if inspect.isabstract(obj):
                    continue
                if obj in providers:
                    raise DependencyError(f"Duplicate DI provider: {obj.__qualname__}")
                providers[obj] = obj
    return providers
