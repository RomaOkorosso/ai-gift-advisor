from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_gift_service
from app.schemas.gifts import Gift
from app.services import GiftService

gift_router = APIRouter(
    prefix="/gift",
    tags=["Gifts"],
)


@gift_router.post("", status_code=status.HTTP_201_CREATED)
async def post_gift(
        gift: Gift,
        service: Annotated[GiftService, Depends(get_gift_service)]
):
    return await service.create_gift_request(gift)
