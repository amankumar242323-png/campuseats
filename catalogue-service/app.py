import os
import random
import time

import requests

from flask import Flask, jsonify, request

import store

from errors import problem


app = Flask(__name__)


SUPPORTED_RESTAURANTS = {
    1,
    2,
    3
}


# =========================================================
# C4 — VALIDATION
# =========================================================

def validate_menu_item(body):

    errors = []

    if not isinstance(body, dict):
        return [["body", "JSON object required"]]

    if not isinstance(
        body.get("restaurantId"),
        int
    ):
        errors.append(
            ["restaurantId", "required integer"]
        )

    if not isinstance(
        body.get("menuId"),
        int
    ):
        errors.append(
            ["menuId", "required integer"]
        )

    if not body.get("name"):
        errors.append(
            ["name", "required"]
        )

    price = body.get("price")

    if (
        not isinstance(price, (int, float))
        or price <= 0
    ):
        errors.append(
            ["price", "must be positive"]
        )

    if (
        "description" in body
        and not isinstance(body["description"], str)
    ):
        errors.append(
            ["description", "must be a string"]
        )

    if (
        "available" in body
        and not isinstance(body["available"], bool)
    ):
        errors.append(
            ["available", "must be boolean"]
        )

    return errors


def validate_availability(body):

    errors = []

    if not isinstance(body, dict):
        return [["body", "JSON object required"]]

    if "available" not in body:
        errors.append(
            ["available", "required"]
        )

    elif not isinstance(
        body["available"],
        bool
    ):
        errors.append(
            ["available", "must be boolean"]
        )

    return errors


# =========================================================
# D — OUTBOUND HTTP CALL
# =========================================================

def notify_orders_service(item):

    """
    Make a real HTTP call to another CampusEats service.

    The service address comes from an environment variable.
    """

    orders_url = os.environ.get(
        "ORDERS_URL"
    )

    if not orders_url:
        return True

    url = (
        orders_url.rstrip("/")
        + "/health"
    )

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = requests.get(
                url,
                timeout=2.0
            )

            # Never retry a 4xx response.
            if 400 <= response.status_code < 500:
                return False

            if response.status_code < 500:
                return True

        except requests.RequestException:

            pass

        if attempt < max_attempts - 1:

            wait = (
                0.5 * (2 ** attempt)
                + random.uniform(0, 0.25)
            )

            time.sleep(wait)

    return False


# =========================================================
# POST /menu-items
# =========================================================

@app.post("/menu-items")
def create_menu_item():

    body = request.get_json(
        silent=True
    )

    # IMPORTANT:
    # Validate BEFORE accessing body fields.
    errors = validate_menu_item(body)

    if errors:

        return problem(
            400,
            "invalid-request",
            "The request body is invalid.",
            errors
        )

    restaurant_id = body["restaurantId"]

    if restaurant_id not in SUPPORTED_RESTAURANTS:

        return problem(
            422,
            "domain-rejected",
            "The specified restaurant does not exist."
        )

    key = request.headers.get(
        "Idempotency-Key"
    )

    if not key:

        return problem(
            400,
            "invalid-request",
            "Idempotency-Key is required."
        )

    # =====================================================
    # C7 — IDEMPOTENCY
    # =====================================================

    previous = store.find_by_key(key)

    if previous:

        return jsonify(
            previous.as_json()
        ), 200

    # =====================================================
    # CREATE
    # =====================================================

    item = store.create(

        restaurant_id=restaurant_id,

        menu_id=body["menuId"],

        name=body["name"],

        description=body.get(
            "description",
            ""
        ),

        price=float(
            body["price"]
        ),

        available=body.get(
            "available",
            True
        ),

        key=key
    )

    # D — outbound call
    # Failure does not invalidate catalogue creation.
    notify_orders_service(item)

    return (
        jsonify(item.as_json()),
        201,
        {
            "Location":
                f"/menu-items/{item.id}"
        }
    )


# =========================================================
# GET /menu-items/{id}
# =========================================================

@app.get("/menu-items/<int:item_id>")
def get_menu_item(item_id):

    item = store.find(item_id)

    if item is None:

        return problem(
            404,
            "item-not-found",
            f"No menu item {item_id}"
        )

    return jsonify(
        item.as_json()
    ), 200


# =========================================================
# GET /menu-items?search=...
# =========================================================

@app.get("/menu-items")
def search_menu_items():

    search_text = request.args.get(
        "search"
    )

    if not search_text:

        return problem(
            400,
            "invalid-request",
            "The search query is required."
        )

    if not search_text.strip():

        return problem(
            400,
            "invalid-request",
            "The search query cannot be empty."
        )

    items = store.search(
        search_text
    )

    return jsonify([
        item.as_json()
        for item in items
    ]), 200


# =========================================================
# GET /restaurants/{restaurant_id}/menu
# =========================================================

@app.get(
    "/restaurants/<int:restaurant_id>/menu"
)
def get_menu(restaurant_id):

    if restaurant_id not in SUPPORTED_RESTAURANTS:

        return problem(
            404,
            "restaurant-not-found",
            f"No restaurant {restaurant_id}"
        )

    items = store.find_by_restaurant(
        restaurant_id
    )

    return jsonify([
        item.as_json()
        for item in items
    ]), 200


# =========================================================
# PATCH /menu-items/{id}/availability
# =========================================================

@app.patch(
    "/menu-items/<int:item_id>/availability"
)
def set_availability(item_id):

    body = request.get_json(
        silent=True
    )

    errors = validate_availability(
        body
    )

    if errors:

        return problem(
            400,
            "invalid-request",
            "The request body is invalid.",
            errors
        )

    item = store.find(
        item_id
    )

    if item is None:

        return problem(
            404,
            "item-not-found",
            f"No menu item {item_id}"
        )

    requested = body["available"]

    # Wrong state = 409.
    if item.available == requested:

        return problem(
            409,
            "state-conflict",
            f"Menu item is already "
            f"{'available' if requested else 'unavailable'}."
        )

    item.available = requested

    return jsonify(
        item.as_json()
    ), 200


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return jsonify({
        "status": "alive"
    }), 200


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8081,
        debug=True
    )