from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class GiftRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid", revalidate_instances="always")

    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=2000)]
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)]


class GiftRecommendations(BaseModel):
    model_config = ConfigDict(extra="forbid", revalidate_instances="always")

    recommendations: Annotated[list[GiftRecommendation], Field(min_length=1, max_length=5)]
