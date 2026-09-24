import asyncio
import json

import pytest

from app.llm.errors import (
    LLMInvalidResponseError,
    LLMProviderError,
    LLMRateLimitError,
    LLMTimeoutError,
    LLMUnavailableError,
)
from app.llm.parsing import parse_recommendations
from app.schemas.gifts import Gift
from app.schemas.recommendations import GiftRecommendation, GiftRecommendations
from app.services.recommendations import GiftRecommendationService


IDEA = {
    "title": "Книга о космосе",
    "description": "Иллюстрированная книга об астрономии",
    "reason": "Получатель интересуется космосом",
}


class JSONProvider:
    def __init__(self, payload):
        self.payload = payload
        self.received = None

    async def recommend(self, gift):
        self.received = gift
        return parse_recommendations(self.payload)


@pytest.fixture
def gift():
    return Gift(budget=3000, description="Друг интересуется космосом")


@pytest.mark.anyio
async def test_service_returns_structured_recommendations(gift):
    provider = JSONProvider(json.dumps({"recommendations": [IDEA]}))
    result = await GiftRecommendationService(provider).recommend(gift)

    assert isinstance(result, GiftRecommendations)
    assert isinstance(result.recommendations[0], GiftRecommendation)
    assert result.model_dump() == {"recommendations": [IDEA]}
    assert provider.received == gift


@pytest.mark.anyio
@pytest.mark.parametrize("payload", [
    "not JSON",
    "",
    "null",
    "[]",
    "{}",
    json.dumps({"recommendations": []}),
    json.dumps({"recommendations": [IDEA] * 6}),
    json.dumps({"recommendations": [{"title": "Only a title"}]}),
    json.dumps({"recommendations": [{**IDEA, "title": "   "}]}),
    json.dumps({"recommendations": [{**IDEA, "reason": 123}]}),
    json.dumps({"recommendations": [{**IDEA, "description": "x" * 2001}]}),
    json.dumps({"recommendations": [{**IDEA, "unexpected": "value"}]}),
    json.dumps({"recommendations": [IDEA], "unexpected": "value"}),
])
async def test_invalid_provider_json_has_safe_error(gift, payload):
    service = GiftRecommendationService(JSONProvider(payload))
    with pytest.raises(LLMInvalidResponseError) as error:
        await service.recommend(gift)
    assert str(error.value) == "Provider returned invalid recommendations"


@pytest.mark.anyio
async def test_service_revalidates_provider_model(gift):
    class InvalidProvider:
        async def recommend(self, gift):
            return GiftRecommendations.model_construct(recommendations=[])

    with pytest.raises(LLMInvalidResponseError):
        await GiftRecommendationService(InvalidProvider()).recommend(gift)


@pytest.mark.anyio
@pytest.mark.parametrize("error_type", [
    LLMTimeoutError,
    LLMUnavailableError,
    LLMRateLimitError,
    LLMProviderError,
    LLMInvalidResponseError,
    RuntimeError,
])
async def test_service_preserves_error_types(gift, error_type):
    error = error_type("Synthetic failure")

    class FailingProvider:
        async def recommend(self, gift):
            raise error

    with pytest.raises(error_type) as caught:
        await GiftRecommendationService(FailingProvider()).recommend(gift)
    assert caught.value is error


class WaitingProvider:
    def __init__(self):
        self.started = asyncio.Event()
        self.stopped = asyncio.Event()

    async def recommend(self, gift):
        self.started.set()
        try:
            await asyncio.Event().wait()
        finally:
            self.stopped.set()


@pytest.mark.anyio
async def test_timeout_cancels_provider(gift):
    provider = WaitingProvider()
    service = GiftRecommendationService(provider, timeout_seconds=0.01)

    with pytest.raises(LLMTimeoutError):
        await service.recommend(gift)
    assert provider.started.is_set()
    assert provider.stopped.is_set()


@pytest.mark.anyio
async def test_external_cancellation_is_not_a_provider_error(gift):
    provider = WaitingProvider()
    service = GiftRecommendationService(provider)
    task = asyncio.create_task(service.recommend(gift))
    try:
        await asyncio.wait_for(provider.started.wait(), timeout=1)
    finally:
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert provider.stopped.is_set()


@pytest.mark.parametrize("timeout", [0, -1, float("inf"), float("nan")])
def test_invalid_timeout_rejected(timeout):
    with pytest.raises(ValueError, match="finite and positive"):
        GiftRecommendationService(JSONProvider("{}"), timeout_seconds=timeout)
