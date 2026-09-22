import pytest

import app as application
import store


@pytest.fixture
def client(monkeypatch):
    store._orders.clear()
    store._idempotency_keys.clear()
    store._next_id = 1

    def fake_check_item(item_id):
        return {
            "id": item_id,
            "name": "Veg Burger",
            "price": 120.0,
            "available": True
        }

    monkeypatch.setattr(
        application,
        "check_item",
        fake_check_item
    )

    return application.app.test_client()


BODY = {
    "studentId": 17,
    "items": [
        {
            "itemId": 1,
            "qty": 2
        }
    ],
    "deliveryAddressId": 5,
    "paymentMethodId": 2
}


def test_create_order(client):
    response = client.post(
        "/orders",
        json=BODY,
        headers={
            "Idempotency-Key": "test-order-1"
        }
    )

    assert response.status_code == 201
    assert response.headers["Location"] == "/orders/1"

    data = response.get_json()

    assert data["orderId"] == 1
    assert data["status"] == "placed"
    assert data["total"] == 240


def test_same_idempotency_key_returns_original(client, monkeypatch):
    calls = {"count": 0}

    def fake_check_item(item_id):
        calls["count"] += 1

        return {
            "id": item_id,
            "name": "Veg Burger",
            "price": 120.0,
            "available": True
        }

    monkeypatch.setattr(
        application,
        "check_item",
        fake_check_item
    )

    headers = {
        "Idempotency-Key": "same-key"
    }

    first = client.post(
        "/orders",
        json=BODY,
        headers=headers
    )

    second = client.post(
        "/orders",
        json=BODY,
        headers=headers
    )

    assert first.status_code == 201
    assert second.status_code == 200

    assert first.get_json()["orderId"] == second.get_json()["orderId"]

    assert calls["count"] == 1


def test_invalid_request_returns_400(client):
    invalid_body = {
        "studentId": "17",
        "items": [],
        "deliveryAddressId": 5,
        "paymentMethodId": 2
    }

    response = client.post(
        "/orders",
        json=invalid_body,
        headers={
            "Idempotency-Key": "invalid-order"
        }
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["type"] == "/errors/invalid-request"
    assert data["status"] == 400
    assert "errors" in data


def test_unknown_order_returns_404(client):
    response = client.get("/orders/999")

    assert response.status_code == 404

    data = response.get_json()

    assert data["type"] == "/errors/order-not-found"
    assert data["status"] == 404