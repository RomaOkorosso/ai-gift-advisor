from pydantic import BaseModel, Field
from typing import Annotated


class Gift(BaseModel):
    budget: Annotated[int, Field(default=0, ge=0)]
    description: Annotated[str, Field(min_length=10)]
