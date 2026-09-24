import pytest

from sqlalchemy import func, select

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

    # Force the GET to load from PostgreSQL rather than the session identity map.
    db_session.expunge_all()
    retrieved = await client.get(f"/gift/{data['id']}")
    assert retrieved.status_code == 200
    assert retrieved.json() == data


@pytest.mark.anyio
async def test_deleted_gift_returns_404(client, db_session):
    gift = GiftRequestModel(budget=100, description="A gift for a friend")
    db_session.add(gift)
    await db_session.commit()
    gift_id = gift.id
    await db_session.delete(gift)
    await db_session.commit()

    response = await client.get(f"/gift/{gift_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Gift request not found"}


@pytest.mark.anyio
async def test_default_budget_and_trimmed_description_are_saved(client, db_session):
    response = await client.post(
        "/gift", json={"description": "  A gift for a friend  "}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["budget"] == 0
    assert data["description"] == "A gift for a friend"

    db_session.expunge_all()
    saved = await db_session.get(GiftRequestModel, data["id"])
    assert saved.budget == 0
    assert saved.description == "A gift for a friend"


@pytest.mark.anyio
async def test_invalid_request_does_not_insert_row(client, db_session):
    count_query = select(func.count()).select_from(GiftRequestModel)
    before = await db_session.scalar(count_query)
    response = await client.post(
        "/gift", json={"budget": 100, "description": "x" * 2001}
    )
    assert response.status_code == 422
    assert await db_session.scalar(count_query) == before
