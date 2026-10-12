
from flask import jsonify

TITLES = {
    "invalid-request": "Invalid request",
    "empty-cart": "Empty cart",
    "item-unavailable": "Item unavailable",
    "payment-declined": "Payment declined",
    "order-not-found": "Order not found",
    "illegal-transition": "Illegal state transition",
    "invalid-address": "Invalid address",
    "not-cancellable": "Order cannot be cancelled",
    "catalogue-unavailable": "Catalogue unavailable",
    "unauthorized": "Unauthorized",
    "not-acceptable": "Not acceptable",
    "unsupported-media-type": "Unsupported media type",
    "rate-limit-exceeded": "Too many requests",
    "precondition-failed": "Precondition failed",
    "method-not-allowed": "Method not allowed",
    "internal-error": "Internal server error",
}


def problem(status: int, code: str, detail: str = "", errors=None):
    body = {
        "type": f"/errors/{code}",
        "title": TITLES.get(code, "Error"),
        "status": status,
        "detail": detail,
    }

    if errors:
        formatted_errors = []

        for error in errors:
            if isinstance(error, (list, tuple)) and len(error) >= 2:
                formatted_errors.append({
                    "field": error[0],
                    "message": error[1],
                })
            elif isinstance(error, dict):
                formatted_errors.append(error)
            else:
                formatted_errors.append({
                    "message": str(error),
                })

        body["errors"] = formatted_errors

    response = jsonify(body)
    response.status_code = status
    response.headers["Content-Type"] = (
        "application/problem+json; charset=utf-8"
    )
    return response
