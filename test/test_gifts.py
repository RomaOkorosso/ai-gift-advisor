from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_gift_without_description():
    res = client.post(
        "/gift",
        json={"budget": 1000},
    )

    assert res.status_code == 422


def test_gift_with_negative_budget():
    res = client.post(
        "/gift",
        json={
            "budget": -100,
            "description": "more than 10 symbols"
        }
    )

    assert res.status_code == 422


def test_gift_with_valid_data():
    res = client.post(
        "/gift",
        json={
            "budget": 1000,
            "description": "more than 10 symbols"
        }
    )

    assert res.json() == {
        "budget": 1000,
        "description": "more than 10 symbols"
    }
