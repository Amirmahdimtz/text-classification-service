"""Allowlisted JSON logging; never interpolate request payloads or exceptions."""
from __future__ import annotations

import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


class SafeJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "event": record.msg if isinstance(record.msg, str) and record.msg in {
                "request_completed", "startup_completed", "startup_failed", "shutdown_completed",
                "readiness_failed", "unhandled_error",
            } else "internal_event",
            "request_id": request_id_var.get(),
        }, ensure_ascii=False)


def configure_logging() -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(SafeJsonFormatter())
    root = logging.getLogger("classification_service")
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    root.propagate = False
