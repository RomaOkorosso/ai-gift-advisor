from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated
from pydantic import ConfigDict


class Gift(BaseModel):
    budget: Annotated[int, Field(default=0, ge=0, le=2147483647)]
    description: Annotated[
        str, StringConstraints(strip_whitespace=True, min_length=10, max_length=2000)
    ]


class GiftResponse(Gift):
    id: int

    model_config = ConfigDict(from_attributes=True)
