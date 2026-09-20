from pydantic import BaseModel, Field
from typing import Annotated
from pydantic import ConfigDict


class Gift(BaseModel):
    budget: Annotated[int, Field(default=0, ge=0)]
    description: Annotated[str, Field(min_length=10)]


class GiftResponse(Gift):
    id: int

    model_config = ConfigDict(from_attributes=True)
