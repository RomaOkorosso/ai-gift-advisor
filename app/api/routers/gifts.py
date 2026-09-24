from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api.dependencies import get_gift_service
from app.schemas.gifts import Gift, GiftResponse
from app.services import GiftService

gift_router = APIRouter(
    prefix="/gift",
    tags=["Gifts"],
)


@gift_router.post("", status_code=status.HTTP_201_CREATED, response_model=GiftResponse)
async def post_gift(
        gift: Gift,
        service: Annotated[GiftService, Depends(get_gift_service)]
):
    return await service.create_gift_request(gift)


@gift_router.get(
    "/{gift_id}",
    response_model=GiftResponse,
    responses={404: {"description": "Gift request not found"}},
)
async def get_gift(
    gift_id: Annotated[int, Path(ge=1, le=2147483647)],
    service: Annotated[GiftService, Depends(get_gift_service)],
):
    gift = await service.get_gift_request(gift_id)
    if gift is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gift request not found",
        )
    return gift
