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


@pytest.mark.anyio
async def test_1_create_gift(db_session):
    gift = GiftRequestModel(
        budget=777777,
        description="Transaction rollback test",
    )

    db_session.add(gift)
    await db_session.commit()

    result = await db_session.execute(
        select(GiftRequestModel).where(
            GiftRequestModel.budget == 777777
        )
    )

    assert result.scalar_one().budget == 777777


@pytest.mark.anyio
async def test_2_gift_was_rolled_back(db_session):
    result = await db_session.execute(
        select(GiftRequestModel).where(
            GiftRequestModel.budget == 777777
        )
    )

    assert result.scalar_one_or_none() is None
