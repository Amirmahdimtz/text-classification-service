import asyncio
from time import sleep
import pytest

from src.infrastructure.text_classifier_provider import (
    InferenceTimeoutError, InferenceUnavailableError, TextClassifierProvider,
)


@pytest.mark.asyncio
async def test_provider_not_ready_and_fail_closed():
    provider = TextClassifierProvider(config_reader=object())  # Test-only injected dependency.
    assert provider.is_ready is False
    with pytest.raises(InferenceUnavailableError, match="not ready"):
        await provider.predict_async(["valid"])
    await provider.close_async()
    assert provider.is_ready is False


@pytest.mark.asyncio
async def test_provider_timeout_keeps_worker_slot_until_completion():
    class SlowTestModel:
        def predict(self, texts):
            sleep(0.1)
            return ["test-only-result"]

    provider = TextClassifierProvider(config_reader=object())
    provider._model = SlowTestModel()  # Test double remains in tests, not production.
    with pytest.raises(InferenceTimeoutError, match="timed out"):
        await provider.predict_async(["valid"], timeout_seconds=0.01)
    assert provider._capacity._value == 1
    with pytest.raises(ValueError, match="batch"):
        await provider.predict_async([""])
    await provider.close_async()


@pytest.mark.asyncio
async def test_provider_does_not_reload_per_request():
    class FastTestModel:
        def __init__(self):
            self.calls = 0
        def predict(self, texts):
            self.calls += 1
            return list(texts)

    provider = TextClassifierProvider(config_reader=object())
    test_model = FastTestModel()
    provider._model = test_model
    assert await provider.predict_async(["text"]) == ["text"]
    assert await provider.predict_async(["next"]) == ["next"]
    assert test_model.calls == 2 and provider.is_ready
    await provider.close_async()


@pytest.mark.asyncio
async def test_provider_close_during_warmup_never_retains_model(monkeypatch, tmp_path):
    """Test-only synchronization reproduces the load/close publication race."""
    from threading import Event
    from src.infrastructure.ml.tfidf_linear_model import TfidfLinearModel

    warming = Event()
    release_warmup = Event()

    class TestOnlyModel:
        def predict(self, texts):
            warming.set()
            if not release_warmup.wait(timeout=5):
                raise RuntimeError("Test-only timeout")
            return []

    monkeypatch.setenv("ML_MODEL_RELEASE_DIR", str(tmp_path.resolve()))
    monkeypatch.setenv("ML_TAXONOMY_VERSION", "test-only")
    monkeypatch.setattr(
        TfidfLinearModel,
        "from_verified_release",
        lambda *a, **kw: TestOnlyModel(),
    )
    provider = TextClassifierProvider(config_reader=object())
    load_task = asyncio.create_task(provider.load_async())
    try:
        assert await asyncio.to_thread(warming.wait, 5)
        close_task = asyncio.create_task(provider.close_async())
        await asyncio.sleep(0)
        assert provider.is_ready is False
        release_warmup.set()
        await asyncio.gather(load_task, close_task)
        assert provider._model is None
        assert provider.is_ready is False
        with pytest.raises(InferenceUnavailableError, match="not ready"):
            await provider.predict_async(["synthetic text"])
    finally:
        release_warmup.set()
        await provider.close_async()


@pytest.mark.asyncio
async def test_provider_close_while_waiting_for_capacity_fails_closed_without_slot_leak():
    """Model may become unavailable after the first readiness check."""
    class TestOnlyModel:
        def predict(self, texts):
            return list(texts)

    provider = TextClassifierProvider(config_reader=object())
    provider._model = TestOnlyModel()  # Test-only model; never a production fallback.
    await provider._capacity.acquire()
    await provider._capacity.acquire()
    request = asyncio.create_task(
        provider.predict_async(["synthetic text"], timeout_seconds=2)
    )
    try:
        # The request has passed initial is_ready and is now waiting for capacity.
        await asyncio.sleep(0)
        assert request.done() is False
        await provider.close_async()
        provider._capacity.release()
        with pytest.raises(InferenceUnavailableError, match="not ready"):
            await request
        # One slot was held by the test; the failed request must release its slot.
        assert provider._capacity._value == 1
    finally:
        if not request.done():
            request.cancel()
            await asyncio.gather(request, return_exceptions=True)
        provider._capacity.release()
        await provider.close_async()
