from fastapi.testclient import TestClient

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


def test_create_gift():
    app.dependency_overrides[get_gift_service] = override_gift_service

    try:
        with TestClient(app) as client:
            response = client.post(
                "/gift",
                json={
                    "budget": 1000,
                    "description": "Друг любит программирование",
                },
            )

        assert response.status_code == 201
        assert response.json() == {
            "id": 42,
            "budget": 1000,
            "description": "Друг любит программирование",
        }

    finally:
        app.dependency_overrides.clear()
