from flask import jsonify


TITLES = {
    "invalid-request": "Invalid request",
    "order-not-found": "Order not found",
    "item-unavailable": "Item unavailable",
    "invalid-address": "Invalid address",
    "not-cancellable": "Order cannot be cancelled",
    "catalogue-unavailable": "Catalogue unavailable",
}


def problem(
    status: int,
    code: str,
    detail: str = "",
    errors=None
):
    body = {
        "type": f"/errors/{code}",
        "title": TITLES.get(code, "Error"),
        "status": status,
        "detail": detail
    }

    if errors:
        body["errors"] = errors

    return jsonify(body), status