"""Bounded, non-blocking model inference provider; no HTTP route is exposed.

The configured, verified artifact is loaded once during explicit warmup.
Absent artifacts/approval always mean NOT READY, never OUT_OF_SCOPE.
"""
from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path

from src.infrastructure.di.inject import inject
from src.infrastructure.utils.config_reader import ConfigReader
from src.infrastructure.ml.tfidf_linear_model import TfidfLinearModel, RawPrediction


class InferenceUnavailableError(RuntimeError):
    """Model is absent, incompatible, or not warmed."""


class InferenceTimeoutError(RuntimeError):
    """Resource saturation or execution exceeded its explicit timeout."""


@inject
class TextClassifierProvider:
    """Single model lifecycle per process, controlled by environment configuration."""

    __di_singleton__ = True

    def __init__(self, config_reader: ConfigReader):
        self._config_reader = config_reader
        self._load_lock = asyncio.Lock()
        self._capacity = asyncio.Semaphore(2)
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="baseline-inference")
        self._model: TfidfLinearModel | None = None
        self._closed = False

    @property
    def is_ready(self) -> bool:
        return self._model is not None and not self._closed

    async def load_async(self) -> None:
        async with self._load_lock:
            if self._closed:
                raise InferenceUnavailableError("Inference provider is shut down")
            if self._model is not None:
                return
            path = os.environ.get("ML_MODEL_RELEASE_DIR", "")
            taxonomy = os.environ.get("ML_TAXONOMY_VERSION", "")
            if not path or not Path(path).is_absolute() or not taxonomy:
                raise InferenceUnavailableError("Configured absolute release path and taxonomy version required")
            try:
                model = await asyncio.to_thread(
                    TfidfLinearModel.from_verified_release, Path(path), taxonomy_version=taxonomy,
                )
                await asyncio.to_thread(model.predict, ["warmup"])
            except Exception:
                raise InferenceUnavailableError("Model load or warmup failed") from None
            self._model = model

    async def predict_async(self, texts: list[str], *, timeout_seconds: float = 10.0) -> list[RawPrediction]:
        if not self.is_ready:
            raise InferenceUnavailableError("Model is not ready")
        if (not isinstance(texts, list) or not 1 <= len(texts) <= 32 or
            any(not isinstance(item, str) or not item.strip() or len(item) > 100_000 for item in texts)):
            raise ValueError("Input batch must contain 1..32 valid bounded text inputs")
        if not 0 < timeout_seconds <= 120:
            raise ValueError("Invalid inference timeout")
        try:
            await asyncio.wait_for(self._capacity.acquire(), timeout_seconds)
        except asyncio.TimeoutError:
            raise InferenceTimeoutError("Inference capacity exhausted") from None
        loop = asyncio.get_running_loop()
        try:
            future = loop.run_in_executor(self._executor, self._model.predict, texts)
        except RuntimeError:
            self._capacity.release()
            raise InferenceUnavailableError("Inference executor is unavailable") from None
        # Release the semaphore only after the real worker returns, even on request timeout.
        future.add_done_callback(lambda completed: self._capacity.release())
        try:
            return await asyncio.wait_for(asyncio.shield(future), timeout_seconds)
        except asyncio.TimeoutError:
            raise InferenceTimeoutError("Model execution timed out") from None
        except asyncio.CancelledError:
            raise
        except Exception:
            raise InferenceUnavailableError("Model inference failed") from None

    async def close_async(self) -> None:
        self._closed = True
        # Wait for any in-flight warmup before clearing the model reference.
        # Without the lock, load_async can install a model after close_async.
        try:
            async with self._load_lock:
                self._model = None
        finally:
            await asyncio.to_thread(self._executor.shutdown, wait=True, cancel_futures=True)
