from sqlalchemy import select
import pytest

from app.models.gift import GiftRequestModel


@pytest.mark.anyio
async def test_create_gift(db_session):
    gift = GiftRequestModel(
        budget=3000,
        description="Test gift description",
    )

    db_session.add(gift)
    await db_session.commit()

    result = await db_session.execute(
        select(GiftRequestModel).where(
            GiftRequestModel.id == gift.id
        )
    )

    saved_gift = result.scalar_one()

    assert saved_gift.budget == 3000
    assert saved_gift.description == "Test gift description"
