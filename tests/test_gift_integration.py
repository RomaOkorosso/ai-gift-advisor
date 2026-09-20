import pytest

from sqlalchemy import select

from app.models.gift import GiftRequestModel


@pytest.mark.anyio
async def test_create_gift_in_database(client, db_session):
    response = await client.post(
        "/gift",
        json={
            "budget": 3000,
            "description": "Подарок для любителя программирования",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["budget"] == 3000
    assert "id" in data

    result = await db_session.execute(
        select(GiftRequestModel).where(
            GiftRequestModel.id == data["id"]
        )
    )

    saved_gift = result.scalar_one()

    assert saved_gift.budget == 3000
    assert saved_gift.description == (
        "Подарок для любителя программирования"
    )
