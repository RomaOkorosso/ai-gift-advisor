from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.gifts import Gift
from app.services import GiftService

gift_router = APIRouter(
    prefix="/gift",
    tags=["Gifts"],
)


@gift_router.post("")
async def post_gift(
        gift: Gift,
        db: Annotated[AsyncSession, Depends(get_db)],
        status_code=status.HTTP_201_CREATED
):
    service = GiftService(db)

    return await service.create_gift_request(gift)
