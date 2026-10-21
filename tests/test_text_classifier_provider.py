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
