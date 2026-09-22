import sys
from pathlib import Path

import pytest

# Add catalogue-service directory to Python import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as application
import store


@pytest.fixture
def client():
    store.reset()
    return application.app.test_client()


BODY = {
    "restaurantId": 1,
    "menuId": 10,
    "name": "Veg Biryani",
    "description": "Campus special",
    "price": 120,
    "available": True
}


def test_create_menu_item(client):
    response = client.post(
        "/menu-items",
        json=BODY,
        headers={"Idempotency-Key": "key-001"}
    )

    assert response.status_code == 201
    assert response.headers["Location"] == f"/menu-items/{response.json['id']}"
    assert response.json["name"] == "Veg Biryani"


def test_same_key_returns_original(client):
    headers = {"Idempotency-Key": "same-key"}

    first = client.post(
        "/menu-items",
        json=BODY,
        headers=headers
    )

    second = client.post(
        "/menu-items",
        json=BODY,
        headers=headers
    )

    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json["id"] == second.json["id"]


def test_invalid_body_returns_400(client):
    response = client.post(
        "/menu-items",
        json={
            "restaurantId": 1,
            "menuId": 10
        },
        headers={"Idempotency-Key": "bad-key"}
    )

    assert response.status_code == 400
    assert response.json["type"] == "/errors/invalid-request"


def test_unknown_item_returns_404(client):
    response = client.get("/menu-items/999")

    assert response.status_code == 404
    assert response.json["status"] == 404