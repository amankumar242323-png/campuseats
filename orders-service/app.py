from flask import Flask, jsonify, request

import store
from errors import problem
from validation import validate_place_order

from catalogue_client import (
    check_item,
    ItemUnavailable,
    CatalogueItemNotFound,
    CatalogueUnavailable,
    CatalogueRejected
)


app = Flask(__name__)


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return jsonify({
        "service": "orders",
        "status": "alive"
    }), 200


# =========================================================
# POST /orders
# =========================================================

@app.post("/orders")
def create_order():

    # -----------------------------------------------------
    # 1. Read request body
    # -----------------------------------------------------

    body = request.get_json(silent=True)

    # -----------------------------------------------------
    # 2. Validate BEFORE accessing body fields
    # -----------------------------------------------------

    errors = validate_place_order(body)

    if errors:
        return problem(
            400,
            "invalid-request",
            "The request body is invalid.",
            errors
        )

    # -----------------------------------------------------
    # 3. Read Idempotency-Key
    # -----------------------------------------------------

    key = request.headers.get("Idempotency-Key")

    if not key:
        return problem(
            400,
            "invalid-request",
            "Idempotency-Key is required."
        )

    # -----------------------------------------------------
    # 4. Check for previous request
    # -----------------------------------------------------

    previous = store.find_by_idempotency_key(key)

    if previous:
        return jsonify(
            previous.as_json()
        ), 200

    # -----------------------------------------------------
    # 5. Check every item with Catalogue Service
    # -----------------------------------------------------

    checked_items = []
    total = 0

    try:

        for item in body["items"]:

            catalogue_item = check_item(
                item["itemId"]
            )

            quantity = item["qty"]

            # Calculate total using Catalogue price
            total += int(
                round(
                    catalogue_item["price"] * quantity
                )
            )

            # Store only required order item information
            checked_items.append({
                "itemId": catalogue_item["id"],
                "name": catalogue_item["name"],
                "qty": quantity,
                "unitPrice": catalogue_item["price"]
            })

    except ItemUnavailable as exc:

        return problem(
            422,
            "item-unavailable",
            str(exc)
        )

    except CatalogueItemNotFound as exc:

        return problem(
            422,
            "item-unavailable",
            str(exc)
        )

    except CatalogueRejected as exc:

        return problem(
            400,
            "invalid-request",
            str(exc)
        )

    except CatalogueUnavailable as exc:

        return problem(
            503,
            "catalogue-unavailable",
            str(exc)
        )

    # -----------------------------------------------------
    # 6. Create order
    # -----------------------------------------------------

    order = store.create_order(
        student_id=body["studentId"],
        items=checked_items,
        delivery_address_id=body["deliveryAddressId"],
        payment_method_id=body["paymentMethodId"],
        total=total,
        status="placed",
        idempotency_key=key
    )

    # -----------------------------------------------------
    # 7. Return created order
    # -----------------------------------------------------

    return (
        jsonify(order.as_json()),
        201,
        {
            "Location": f"/orders/{order.id}"
        }
    )


# =========================================================
# GET /orders/{id}
# =========================================================

@app.get("/orders/<int:order_id>")
def get_order(order_id):

    order = store.find_order(order_id)

    if order is None:
        return problem(
            404,
            "order-not-found",
            f"No order {order_id}"
        )

    return jsonify(
        order.as_json()
    ), 200


# =========================================================
# GET /orders?status=...
# =========================================================

@app.get("/orders")
def list_orders():

    status = request.args.get("status")

    # -----------------------------------------------------
    # No filter → return all orders
    # -----------------------------------------------------

    if status is None:

        orders = store.find_all()

    # -----------------------------------------------------
    # Filter by status
    # -----------------------------------------------------

    else:

        if status not in {
            "placed",
            "cancelled"
        }:
            return problem(
                400,
                "invalid-request",
                "Status must be 'placed' or 'cancelled'."
            )

        orders = store.find_by_status(
            status
        )

    return jsonify([
        order.as_json()
        for order in orders
    ]), 200


# =========================================================
# POST /orders/{id}/cancellation
# =========================================================

@app.post("/orders/<int:order_id>/cancellation")
def cancel_order(order_id):

    order = store.find_order(order_id)

    # -----------------------------------------------------
    # 1. Order does not exist
    # -----------------------------------------------------

    if order is None:

        return problem(
            404,
            "order-not-found",
            f"No order {order_id}"
        )

    # -----------------------------------------------------
    # 2. Order exists but cannot be cancelled
    # -----------------------------------------------------

    if order.status != "placed":

        return problem(
            409,
            "not-cancellable",
            f"Order is already {order.status}."
        )

    # -----------------------------------------------------
    # 3. Cancel order
    # -----------------------------------------------------

    store.cancel_order(order)

    return jsonify({
        "orderId": order.id,
        "status": order.status
    }), 202


# =========================================================
# MALFORMED REQUEST
# =========================================================

@app.errorhandler(400)
def bad_request(error):

    return problem(
        400,
        "invalid-request",
        "Malformed request."
    )


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8082,
        debug=True
    )