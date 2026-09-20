from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.gifts import GiftService


def get_gift_service(
        db: Annotated[AsyncSession, Depends(get_db)],
) -> GiftService:
    return GiftService(db)
