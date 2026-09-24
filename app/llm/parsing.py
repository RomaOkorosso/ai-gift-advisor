from pydantic import ValidationError

from app.llm.errors import LLMInvalidResponseError
from app.schemas.recommendations import GiftRecommendations


def parse_recommendations(raw_response: str) -> GiftRecommendations:
    """Validate provider JSON without exposing its contents in the error message."""
    try:
        return GiftRecommendations.model_validate_json(raw_response)
    except ValidationError as exc:
        raise LLMInvalidResponseError("Provider returned invalid recommendations") from exc
