import pytest

from httpx import ASGITransport, AsyncClient

from app.api.dependencies import get_gift_service
from app.main import app


class FakeGiftService:
    async def create_gift_request(self, gift):
        return {
            "id": 42,
            "budget": gift.budget,
            "description": gift.description,
        }


def override_gift_service():
    return FakeGiftService()


@pytest.mark.anyio
@pytest.mark.parametrize("payload", [
    {"budget": -1, "description": "Valid description"},
    {"budget": 2147483648, "description": "Valid description"},
    {"budget": 100, "description": "x" * 2001},
    {"budget": 100, "description": " " * 10},
    {"budget": 100, "description": "short"},
    {"budget": 100},
    {"budget": None, "description": "Valid description"},
    {"budget": 1.5, "description": "Valid description"},
    {"budget": "invalid", "description": "Valid description"},
])
async def test_invalid_gift_returns_422(payload):
    class RejectingService:
        async def create_gift_request(self, gift):
            pytest.fail("Invalid request must not reach the service")

    app.dependency_overrides[get_gift_service] = RejectingService
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/gift", json=payload)
        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(get_gift_service, None)


@pytest.mark.anyio
async def test_gift_database_boundaries():
    app.dependency_overrides[get_gift_service] = override_gift_service
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/gift", json={"budget": 2147483647, "description": "x" * 2000}
            )
        assert response.status_code == 201
        assert response.json()["budget"] == 2147483647
        assert len(response.json()["description"]) == 2000
    finally:
        app.dependency_overrides.pop(get_gift_service, None)


@pytest.mark.anyio
async def test_create_gift():
    app.dependency_overrides[get_gift_service] = override_gift_service

    try:
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as client:
            response = await client.post(
                "/gift",
                json={
                    "budget": 1000,
                    "description": "Друг любит программирование",
                },
            )
    finally:
        app.dependency_overrides.pop(get_gift_service, None)

    assert response.status_code == 201
    assert response.json() == {
        "id": 42,
        "budget": 1000,
        "description": "Друг любит программирование",
    }


@pytest.mark.anyio
@pytest.mark.parametrize("gift_id", ["0", "-1", "2147483648", "abc", "1.5"])
async def test_invalid_gift_id_returns_422(gift_id):
    class RejectingService:
        async def get_gift_request(self, gift_id):
            pytest.fail("Invalid ID must not reach the service")

    app.dependency_overrides[get_gift_service] = RejectingService
    try:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get(f"/gift/{gift_id}")
        assert response.status_code == 422
    finally:
        app.dependency_overrides.pop(get_gift_service, None)
