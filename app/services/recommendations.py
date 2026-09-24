import asyncio
import math

from pydantic import ValidationError

from app.llm.errors import LLMInvalidResponseError, LLMTimeoutError
from app.llm.provider import LLMProvider
from app.schemas.gifts import Gift
from app.schemas.recommendations import GiftRecommendations


class GiftRecommendationService:
    def __init__(self, provider: LLMProvider, *, timeout_seconds: float = 30.0):
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        self.provider = provider
        self.timeout_seconds = timeout_seconds

    async def recommend(self, gift: Gift) -> GiftRecommendations:
        try:
            async with asyncio.timeout(self.timeout_seconds):
                result = await self.provider.recommend(gift)
        except TimeoutError as exc:
            raise LLMTimeoutError("Recommendation generation timed out") from exc

        try:
            return GiftRecommendations.model_validate(result)
        except ValidationError as exc:
            raise LLMInvalidResponseError("Provider returned invalid recommendations") from exc
