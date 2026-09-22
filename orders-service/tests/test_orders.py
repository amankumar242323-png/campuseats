import pytest

import app as application
import store


AUTH_HEADERS = {
    "Authorization": "Bearer demo-token"
}


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

    application._rate_limits.clear()

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


# ============================================================
# CREATE ORDER
# ============================================================

def test_create_order(client):

    headers = {
        **AUTH_HEADERS,
        "Idempotency-Key": "test-order-1"
    }

    response = client.post(
        "/orders",
        json=BODY,
        headers=headers
    )

    assert response.status_code == 201

    assert response.headers["Location"] == "/orders/1"

    assert response.headers[
        "Content-Type"
    ].startswith("application/json")

    data = response.get_json()

    assert data["orderId"] == 1

    assert data["status"] == "placed"

    assert data["total"] == 240


# ============================================================
# IDEMPOTENCY KEY
# ============================================================

def test_same_idempotency_key_returns_original(client, monkeypatch):

    calls = {
        "count": 0
    }

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
        **AUTH_HEADERS,
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

    assert (
        first.get_json()["orderId"]
        == second.get_json()["orderId"]
    )

    # Catalogue was checked only once.
    assert calls["count"] == 1


# ============================================================
# INVALID REQUEST
# ============================================================

def test_invalid_request_returns_400(client):

    invalid_body = {
        "studentId": "17",
        "items": [],
        "deliveryAddressId": 5,
        "paymentMethodId": 2
    }

    headers = {
        **AUTH_HEADERS,
        "Idempotency-Key": "invalid-order"
    }

    response = client.post(
        "/orders",
        json=invalid_body,
        headers=headers
    )

    assert response.status_code == 400

    data = response.get_json()

    assert data["type"] == "/errors/invalid-request"

    assert data["status"] == 400

    assert "errors" in data


# ============================================================
# UNKNOWN ORDER
# ============================================================

def test_unknown_order_returns_404(client):

    response = client.get(
        "/orders/999",
        headers=AUTH_HEADERS
    )

    assert response.status_code == 404

    data = response.get_json()

    assert data["type"] == "/errors/order-not-found"

    assert data["status"] == 404


# ============================================================
# MISSING AUTHORIZATION
# ============================================================

def test_missing_authorization_returns_401(client):

    response = client.get(
        "/orders/1"
    )

    assert response.status_code == 401

    data = response.get_json()

    assert data["type"] == "/errors/unauthorized"

    assert data["status"] == 401


# ============================================================
# OPTIONS
# ============================================================

def test_options_orders_returns_allow(client):

    response = client.options(
        "/orders"
    )

    assert response.status_code == 204

    assert response.headers["Allow"] == (
        "GET, POST, OPTIONS"
    )


def test_options_single_order_returns_allow(client):

    response = client.options(
        "/orders/1"
    )

    assert response.status_code == 204

    assert response.headers["Allow"] == (
        "GET, PATCH, OPTIONS"
    )


# ============================================================
# CREATE + GET + ETAG
# ============================================================

def test_get_order_returns_etag(client):

    create_headers = {
        **AUTH_HEADERS,
        "Idempotency-Key": "etag-order"
    }

    create_response = client.post(
        "/orders",
        json=BODY,
        headers=create_headers
    )

    assert create_response.status_code == 201

    get_response = client.get(
        "/orders/1",
        headers=AUTH_HEADERS
    )

    assert get_response.status_code == 200

    assert "ETag" in get_response.headers

    etag = get_response.headers["ETag"]

    assert etag.startswith('"')

    assert etag.endswith('"')


# ============================================================
# CONDITIONAL GET — 304
# ============================================================

def test_if_none_match_returns_304(client):

    create_headers = {
        **AUTH_HEADERS,
        "Idempotency-Key": "conditional-order"
    }

    client.post(
        "/orders",
        json=BODY,
        headers=create_headers
    )

    first_get = client.get(
        "/orders/1",
        headers=AUTH_HEADERS
    )

    etag = first_get.headers["ETag"]

    second_get = client.get(
        "/orders/1",
        headers={
            **AUTH_HEADERS,
            "If-None-Match": etag
        }
    )

    assert second_get.status_code == 304

    assert second_get.data == b""

    assert second_get.headers["ETag"] == etag


# ============================================================
# CONDITIONAL WRITE — 412
# ============================================================

def test_if_match_mismatch_returns_412(client):

    create_headers = {
        **AUTH_HEADERS,
        "Idempotency-Key": "write-order"
    }

    client.post(
        "/orders",
        json=BODY,
        headers=create_headers
    )

    response = client.patch(
        "/orders/1",
        json={
            "status": "cancelled"
        },
        headers={
            **AUTH_HEADERS,
            "Content-Type": "application/json",
            "If-Match": '"old-etag"'
        }
    )

    assert response.status_code == 412

    data = response.get_json()

    assert data["type"] == "/errors/precondition-failed"

    assert data["status"] == 412


# ============================================================
# CONDITIONAL WRITE — SUCCESS
# ============================================================

def test_if_match_correct_updates_order(client):

    create_headers = {
        **AUTH_HEADERS,
        "Idempotency-Key": "successful-update"
    }

    client.post(
        "/orders",
        json=BODY,
        headers=create_headers
    )

    get_response = client.get(
        "/orders/1",
        headers=AUTH_HEADERS
    )

    etag = get_response.headers["ETag"]

    update_response = client.patch(
        "/orders/1",
        json={
            "status": "cancelled"
        },
        headers={
            **AUTH_HEADERS,
            "Content-Type": "application/json",
            "If-Match": etag
        }
    )

    assert update_response.status_code == 200

    data = update_response.get_json()

    assert data["orderId"] == 1

    assert data["status"] == "cancelled"

    assert "ETag" in update_response.headers

    assert (
        update_response.headers["ETag"]
        != etag
    )


# ============================================================
# CORS
# ============================================================

def test_cors_headers_are_present(client):

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.headers["Access-Control-Allow-Origin"]
        == "*"
    )

    assert (
        "GET"
        in response.headers[
            "Access-Control-Allow-Methods"
        ]
    )


# ============================================================
# SECURITY HEADERS
# ============================================================

def test_security_headers_are_present(client):

    response = client.get(
        "/health"
    )

    assert (
        response.headers[
            "X-Content-Type-Options"
        ]
        == "nosniff"
    )

    assert (
        "max-age=31536000"
        in response.headers[
            "Strict-Transport-Security"
        ]
    )


# ============================================================
# ACCEPT HEADER
# ============================================================

def test_unsupported_accept_returns_406(client):

    response = client.get(
        "/health",
        headers={
            "Accept": "text/html"
        }
    )

    assert response.status_code == 406


# ============================================================
# RATE LIMIT HEADERS
# ============================================================

def test_rate_limit_headers_are_present(client):

    response = client.get(
        "/health"
    )

    assert "X-RateLimit-Limit" in response.headers

    assert "X-RateLimit-Remaining" in response.headers