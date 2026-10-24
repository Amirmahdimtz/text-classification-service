"""ASGI factory, lifecycle, redacted errors, liveness and DB readiness."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.application.web import WebService
from src.host.observability import configure_logging, request_id_var
from src.infrastructure.context.sql_db.psql_dbcontext import PsqlDbContext
from src.infrastructure.di.bootstrap import bootstrap_di, resolve, shutdown_di
from src.infrastructure.utils.config_reader import ConfigReader

logger = logging.getLogger("classification_service")


def create_app() -> FastAPI:
    configure_logging()
    bootstrap_di()
    try:
        config = resolve(ConfigReader)
        web = resolve(WebService)
    except Exception:
        shutdown_di()
        raise

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        database = None
        try:
            database = resolve(PsqlDbContext)
            if not await database.ping_async():
                raise RuntimeError("Database is not ready")
            app.state.db = database
            logger.info("startup_completed")
            yield
        except Exception:
            logger.error("startup_failed")
            raise
        finally:
            if database is not None:
                await database.close_async()
            shutdown_di()
            logger.info("shutdown_completed")

    app = FastAPI(
        title="Text Classification Service", version=config.get("app.version"),
        lifespan=lifespan,
        docs_url=None, redoc_url=None, openapi_url=None,
    )

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = str(uuid4())
        token = request_id_var.set(request_id)
        try:
            try:
                response = await call_next(request)
            except Exception:
                logger.error("unhandled_error")
                response = JSONResponse(
                    status_code=500,
                    content={"error": {"code": "INTERNAL_ERROR", "request_id": request_id}},
                )
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["Referrer-Policy"] = "no-referrer"
            response.headers["Cache-Control"] = "no-store"
            logger.info("request_completed")
            return response
        finally:
            # Cancellation or an unexpected error must never retain a request ID.
            request_id_var.reset(token)

    @app.get("/health/live", include_in_schema=False)
    async def liveness():
        return {"status": "alive"}

    @app.get("/health/ready", include_in_schema=False)
    async def readiness(request: Request):
        db = getattr(request.app.state, "db", None)
        try:
            is_ready = db is not None and await db.ping_async()
        except Exception:
            # Unexpected driver errors still mean unavailable, not a 500 or ready.
            is_ready = False
        if not is_ready:
            logger.warning("readiness_failed")
            return JSONResponse(status_code=503, content={"status": "not_ready"})
        return {"status": "ready"}

    web.mount(app)
    return app
