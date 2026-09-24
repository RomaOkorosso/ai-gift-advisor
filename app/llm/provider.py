from typing import Protocol

from app.schemas.gifts import Gift
from app.schemas.recommendations import GiftRecommendations


class LLMProvider(Protocol):
    async def recommend(self, gift: Gift) -> GiftRecommendations:
        """Generate validated recommendations without database or HTTP coupling.

        Adapters own prompt construction and SDK-specific details. Translate
        expected SDK failures into the errors in app.llm.errors; leave application
        bugs and cancellation untouched. Implementations must use cancellable
        async I/O and release resources when cancelled. A future fallback wrapper
        can implement this same interface and select errors explicitly.
        """
        ...
