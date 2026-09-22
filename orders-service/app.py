import gzip
import hashlib
import json
import os
import time

from flask import Flask, jsonify, request, make_response

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


# ============================================================
# Configuration
# ============================================================

RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "60"))
RATE_WINDOW = 60

_rate_limits = {}


# ============================================================
# Helper Functions
# ============================================================

def json_response(data, status=200, headers=None):
    response = make_response(jsonify(data), status)

    if headers:
        for key, value in headers.items():
            response.headers[key] = value

    return response


def calculate_etag(order):
    """
    Generate an ETag from the current order representation.
    ETag changes whenever the public representation changes.
    """
    payload = json.dumps(
        order.as_json(),
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")

    digest = hashlib.sha256(payload).hexdigest()

    return f'"{digest}"'


def is_json_request():
    content_type = request.headers.get("Content-Type", "")

    return (
        content_type.startswith("application/json")
        or content_type == ""
    )


def accepts_json():
    accept = request.headers.get("Accept")

    if not accept:
        return True

    accepted_types = [
        item.strip().split(";")[0].strip()
        for item in accept.split(",")
    ]

    return (
        "*/*" in accepted_types
        or "application/json" in accepted_types
        or "application/*+json" in accepted_types
    )


def require_authorization():
    """
    Assignment requirement:
    Protected endpoints require:
        Authorization: Bearer <token>

    No real authentication system is implemented.
    """

    authorization = request.headers.get("Authorization", "").strip()

    if not authorization:
        return problem(
            401,
            "unauthorized",
            "Authorization header is required."
        )

    if not authorization.startswith("Bearer "):
        return problem(
            401,
            "unauthorized",
            "Authorization must use Bearer token format."
        )

    token = authorization[7:].strip()

    if not token:
        return problem(
            401,
            "unauthorized",
            "Bearer token cannot be empty."
        )

    return None


def check_rate_limit():
    """
    Simple per-client in-memory rate limit.
    """

    client = request.remote_addr or "unknown"
    now = time.time()

    record = _rate_limits.get(client)

    if record is None or now - record["start"] >= RATE_WINDOW:
        record = {
            "start": now,
            "count": 0
        }
        _rate_limits[client] = record

    record["count"] += 1

    remaining = max(RATE_LIMIT - record["count"], 0)

    if record["count"] > RATE_LIMIT:
        retry_after = max(
            1,
            int(RATE_WINDOW - (now - record["start"]))
        )

        response = problem(
            429,
            "rate-limit-exceeded",
            "Rate limit exceeded."
        )

        response[0].headers["Retry-After"] = str(retry_after)
        response[0].headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        response[0].headers["X-RateLimit-Remaining"] = "0"

        return response

    return {
        "limit": RATE_LIMIT,
        "remaining": remaining
    }


# ============================================================
# Request Processing
# ============================================================

@app.before_request
def before_request_checks():

    # OPTIONS must work without authentication because browsers
    # use it for CORS preflight.
    if request.method == "OPTIONS":
        return None

    # Accept negotiation applies to all JSON API responses,
    # including the public health endpoint.
    if not accepts_json():
        return problem(
            406,
            "not-acceptable",
            "Only application/json responses are supported."
        )

    # Health endpoint is public.
    if request.path == "/health":
        rate_result = check_rate_limit()

        if rate_result:
            request.rate_limit = rate_result

        return None

    # Protected order endpoints.
    if request.path.startswith("/orders"):
        auth_error = require_authorization()

        if auth_error:
            return auth_error

    # Rate limiting.
    rate_result = check_rate_limit()

    if rate_result:
        request.rate_limit = rate_result
# ============================================================
# Common Response Headers
# ============================================================

@app.after_request
def add_response_headers(response):

    # JSON Content-Type for JSON responses.
    if (
        response.status_code not in (204, 304)
        and response.get_data()
        and response.mimetype == "application/json"
    ):
        response.headers["Content-Type"] = "application/json"

    # Rate limit headers.
    rate_info = getattr(request, "rate_limit", None)

    if rate_info:
        response.headers["X-RateLimit-Limit"] = str(
            rate_info["limit"]
        )

        response.headers["X-RateLimit-Remaining"] = str(
            rate_info["remaining"]
        )

    # CORS headers.
    response.headers["Access-Control-Allow-Origin"] = "*"

    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PATCH, OPTIONS"
    )

    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Accept, Authorization, "
        "Idempotency-Key, If-None-Match, If-Match, "
        "X-HTTP-Method-Override"
    )

    response.headers["Access-Control-Expose-Headers"] = (
        "Location, ETag, X-RateLimit-Limit, "
        "X-RateLimit-Remaining, Retry-After"
    )

    # Security headers.
    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    # Gzip for sufficiently large JSON responses.
    accept_encoding = request.headers.get(
        "Accept-Encoding",
        ""
    )

    if (
        "gzip" in accept_encoding.lower()
        and response.status_code not in (204, 304)
        and response.mimetype == "application/json"
        and response.content_length
        and response.content_length > 1024
        and "Content-Encoding" not in response.headers
    ):
        compressed = gzip.compress(response.get_data())

        response.set_data(compressed)
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = str(len(compressed))
        response.headers["Vary"] = "Accept-Encoding"

    return response


# ============================================================
# Health
# ============================================================

@app.get("/health")
def health():

    return json_response({
        "service": "orders",
        "status": "alive"
    })


# ============================================================
# OPTIONS — Orders Collection
# ============================================================

@app.route("/orders", methods=["OPTIONS"])
def orders_options():

    response = make_response("", 204)

    response.headers["Allow"] = "GET, POST, OPTIONS"

    return response


# ============================================================
# OPTIONS — Individual Order
# ============================================================

@app.route("/orders/<int:order_id>", methods=["OPTIONS"])
def order_options(order_id):

    response = make_response("", 204)

    response.headers["Allow"] = "GET, PATCH, OPTIONS"

    return response


# ============================================================
# OPTIONS — Cancellation
# ============================================================

@app.route(
    "/orders/<int:order_id>/cancellation",
    methods=["OPTIONS"]
)
def cancellation_options(order_id):

    response = make_response("", 204)

    response.headers["Allow"] = "POST, OPTIONS"

    return response


# ============================================================
# POST /orders
# ============================================================

@app.post("/orders")
def create_order():

    # Content-Type validation.
    if not is_json_request():

        return problem(
            400,
            "invalid-request",
            "Content-Type must be application/json."
        )

    body = request.get_json(silent=True)

    errors = validate_place_order(body)

    if errors:

        return problem(
            400,
            "invalid-request",
            "The request body is invalid.",
            errors
        )

    # Idempotency-Key is mandatory.
    key = request.headers.get("Idempotency-Key")

    if not key:

        return problem(
            400,
            "invalid-request",
            "Idempotency-Key is required."
        )

    # --------------------------------------------------------
    # Idempotency check
    # --------------------------------------------------------

    previous = store.find_by_idempotency_key(key)

    if previous:

        response = json_response(
            previous.as_json(),
            200
        )

        response.headers["Location"] = (
            f"/orders/{previous.id}"
        )

        response.headers["Cache-Control"] = "no-store"

        return response

    # --------------------------------------------------------
    # Catalogue validation
    # --------------------------------------------------------

    checked_items = []
    total = 0

    try:

        for item in body["items"]:

            catalogue_item = check_item(
                item["itemId"]
            )

            quantity = item["qty"]

            total += int(
                round(
                    catalogue_item["price"] * quantity
                )
            )

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

    # --------------------------------------------------------
    # Create order
    # --------------------------------------------------------

    order = store.create_order(

        student_id=body["studentId"],

        items=checked_items,

        delivery_address_id=body[
            "deliveryAddressId"
        ],

        payment_method_id=body[
            "paymentMethodId"
        ],

        total=total,

        status="placed",

        idempotency_key=key
    )

    response = json_response(
        order.as_json(),
        201
    )

    response.headers["Location"] = (
        f"/orders/{order.id}"
    )

    response.headers["Cache-Control"] = "no-store"

    return response


# ============================================================
# GET /orders
# ============================================================

@app.get("/orders")
def list_orders():

    status = request.args.get("status")

    if status is None:

        orders = store.find_all()

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

    response = json_response(
        [order.as_json() for order in orders],
        200
    )

    response.headers["Cache-Control"] = (
        "no-store"
    )

    return response


# ============================================================
# GET /orders/{id}
# ============================================================

@app.get("/orders/<int:order_id>")
def get_order(order_id):

    order = store.find_order(order_id)

    if order is None:

        return problem(
            404,
            "order-not-found",
            f"No order {order_id}"
        )

    etag = calculate_etag(order)

    # --------------------------------------------------------
    # Conditional GET - If-None-Match
    # --------------------------------------------------------

    if_none_match = request.headers.get(
        "If-None-Match",
        ""
    ).strip()

    # Support both:
    # If-None-Match: "etag"
    # If-None-Match: etag
    normalized_if_none_match = if_none_match.strip('"')

    normalized_etag = etag.strip('"')

    if (
        normalized_if_none_match == normalized_etag
        or if_none_match == "*"
    ):

        response = make_response("", 304)

        response.headers["ETag"] = etag

        response.headers["Cache-Control"] = (
            "no-store"
        )

        return response

    # --------------------------------------------------------
    # Normal GET
    # --------------------------------------------------------

    response = json_response(
        order.as_json(),
        200
    )

    response.headers["ETag"] = etag

    response.headers["Cache-Control"] = (
        "no-store"
    )

    return response
# ============================================================
# PATCH /orders/{id}
# ============================================================

@app.patch("/orders/<int:order_id>")
def update_order_status(order_id):

    order = store.find_order(order_id)

    if order is None:

        return problem(
            404,
            "order-not-found",
            f"No order {order_id}"
        )

    # --------------------------------------------------------
    # Current ETag
    # --------------------------------------------------------

    etag = calculate_etag(order)

    # --------------------------------------------------------
    # If-Match
    # --------------------------------------------------------

    if_match = request.headers.get(
        "If-Match",
        ""
    ).strip()

    normalized_if_match = if_match.strip('"')
    normalized_etag = etag.strip('"')

    if (
        normalized_if_match != normalized_etag
        and if_match != "*"
    ):

        return problem(
            412,
            "precondition-failed",
            "The order has changed. Refresh the resource and retry."
        )

    # --------------------------------------------------------
    # JSON validation
    # --------------------------------------------------------

    if not is_json_request():

        return problem(
            400,
            "invalid-request",
            "Content-Type must be application/json."
        )

    body = request.get_json(
        silent=True
    )

    if not isinstance(
        body,
        dict
    ):

        return problem(
            400,
            "invalid-request",
            "Request body must be a JSON object."
        )

    new_status = body.get(
        "status"
    )

    allowed_statuses = {
        "placed",
        "cancelled"
    }

    if new_status not in allowed_statuses:

        return problem(
            422,
            "invalid-request",
            "Status must be placed or cancelled."
        )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    store.update_order_status(
        order,
        new_status
    )

    # --------------------------------------------------------
    # New ETag after modification
    # --------------------------------------------------------

    new_etag = calculate_etag(
        order
    )

    response = json_response(
        order.as_json(),
        200
    )

    response.headers["ETag"] = new_etag

    response.headers["Cache-Control"] = (
        "no-store"
    )

    return response

# ============================================================
# X-HTTP-Method-Override fallback
# ============================================================

@app.post("/orders/<int:order_id>")
def method_override(order_id):

    override = request.headers.get(
        "X-HTTP-Method-Override",
        ""
    ).upper()

    if override == "PATCH":

        return update_order_status(
            order_id
        )

    return problem(
        400,
        "invalid-request",
        "Unsupported X-HTTP-Method-Override."
    )


# ============================================================
# POST /orders/{id}/cancellation
# ============================================================

@app.post("/orders/<int:order_id>/cancellation")
def cancel_order(order_id):

    order = store.find_order(order_id)

    if order is None:

        return problem(
            404,
            "order-not-found",
            f"No order {order_id}"
        )

    if order.status != "placed":

        return problem(
            409,
            "not-cancellable",
            f"Order is already {order.status}."
        )

    store.cancel_order(order)

    response = json_response({
        "orderId": order.id,
        "status": order.status
    }, 202)

    response.headers["Cache-Control"] = "no-store"

    return response


# ============================================================
# Error Handlers
# ============================================================

@app.errorhandler(400)
def bad_request(error):

    return problem(
        400,
        "invalid-request",
        "Malformed request."
    )


@app.errorhandler(405)
def method_not_allowed(error):

    return problem(
        405,
        "method-not-allowed",
        "HTTP method is not allowed for this resource."
    )


@app.errorhandler(406)
def not_acceptable(error):

    return problem(
        406,
        "not-acceptable",
        "Requested response format is not supported."
    )


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=8082,
        debug=True
    )