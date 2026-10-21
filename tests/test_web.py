from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
from fastapi import APIRouter, FastAPI

import src.application.web as web_module
from src.application.web import WebService
from src.host.app import create_app
from src.infrastructure.di.bootstrap import bootstrap_di, resolve
from src.infrastructure.di.inject import DependencyError
from src.infrastructure.utils.config_reader import ConfigReader


@pytest.mark.asyncio
async def test_liveness_independent_of_readiness_and_safe_headers():
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        live = await client.get("/health/live")
        ready = await client.get("/health/ready")
    assert live.status_code == 200 and live.json() == {"status": "alive"}
    assert ready.status_code == 503 and ready.json() == {"status": "not_ready"}
    assert "X-Request-ID" in live.headers
    assert live.headers["X-Content-Type-Options"] == "nosniff"
    assert "/api/v1/text_classification/classify" not in [r.path for r in app.routes]


def test_controller_autodiscovery_prefix_and_contract(tmp_path, monkeypatch):
    bootstrap_di()
    root = tmp_path / "application"
    feature = root / "sample_feature"
    feature.mkdir(parents=True)
    (feature / "sample_feature_controller.py").write_text("", encoding="utf-8")

    class SampleFeatureController:
        def api(self):
            router = APIRouter()

            @router.get("/check")
            def check():
                return {"ok": True}

            return router

    monkeypatch.setattr(web_module, "__file__", str(root / "web.py"))
    real_import = web_module.importlib.import_module
    monkeypatch.setattr(web_module.importlib, "import_module", lambda name: SimpleNamespace(SampleFeatureController=SampleFeatureController) if name.endswith("sample_feature_controller") else real_import(name))
    app = FastAPI()
    WebService(resolve(ConfigReader)).mount(app)
    assert "/api/v1/sample_feature/check" in [route.path for route in app.routes]


def test_controller_import_error_is_not_silenced(tmp_path, monkeypatch):
    bootstrap_di()
    root = tmp_path / "application"
    feature = root / "broken"
    feature.mkdir(parents=True)
    (feature / "broken_controller.py").write_text("", encoding="utf-8")
    monkeypatch.setattr(web_module, "__file__", str(root / "web.py"))

    def fail(_):
        raise ImportError("test fixture import failure")

    monkeypatch.setattr(web_module.importlib, "import_module", fail)
    with pytest.raises(DependencyError, match="Controller import failed"):
        WebService(resolve(ConfigReader)).mount(FastAPI())
