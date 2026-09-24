from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gift import GiftRequestModel
from app.schemas.gifts import Gift


class GiftService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_gift_request(self, gift_id: int) -> GiftRequestModel | None:
        return await self.db.get(GiftRequestModel, gift_id)

    async def create_gift_request(
            self,
            gift: Gift,
    ) -> GiftRequestModel:
        gift_request = GiftRequestModel(
            budget=gift.budget,
            description=gift.description,
        )

        self.db.add(gift_request)

        await self.db.commit()
        await self.db.refresh(gift_request)

        return gift_request
