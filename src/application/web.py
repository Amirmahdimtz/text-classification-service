"""Strict convention-based FastAPI controller discovery."""
from __future__ import annotations

import importlib
import inspect
from pathlib import Path

from fastapi import APIRouter, FastAPI

from src.infrastructure.di.bootstrap import resolve
from src.infrastructure.di.inject import DependencyError, inject
from src.infrastructure.utils.config_reader import ConfigReader


@inject
class WebService:
    def __init__(self, config_reader: ConfigReader):
        self._api_prefix = config_reader.get_api_prefix()

    def mount(self, app: FastAPI) -> None:
        root = Path(__file__).resolve().parent
        for directory in sorted(root.iterdir()):
            if not directory.is_dir() or directory.name.startswith("_") or directory.name in ("dtos", "sso"):
                continue
            feature = directory.name
            file = directory / f"{feature}_controller.py"
            if not file.exists():
                continue
            module_name = f"src.application.{feature}.{feature}_controller"
            try:
                module = importlib.import_module(module_name)
            except Exception as exc:
                raise DependencyError(f"Controller import failed: {module_name}") from exc
            expected = "".join(part.capitalize() for part in feature.split("_")) + "Controller"
            controller_class = getattr(module, expected, None)
            if not inspect.isclass(controller_class) or not callable(getattr(controller_class, "api", None)):
                raise DependencyError(f"Invalid controller convention: {module_name}.{expected}")
            if controller_class.__dict__.get("__di_provider__"):
                controller = resolve(controller_class)
            else:
                controller = controller_class()
            router = controller.api()
            if not isinstance(router, APIRouter):
                raise DependencyError(f"Controller api() must return APIRouter: {module_name}")
            if router.prefix:
                raise DependencyError(f"Controller must not repeat the feature prefix: {module_name}")
            app.include_router(router, prefix=f"{self._api_prefix}/{feature}")
