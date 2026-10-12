import hashlib
import json
import os
import re
import time

from flask import Flask, jsonify, make_response, request

import store
from catalogue_client import (
    CatalogueItemNotFound,
    CatalogueRejected,
    CatalogueUnavailable,
    ItemUnavailable,
    check_item,
)
from errors import problem
from validation import validate_place_order


app = Flask(__name__)

RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "100"))
RATE_WINDOW = 60
_rate_limits: dict[str, dict[str, float | int]] = {}


def json_response(data, status=200, headers=None):
    response = make_response(jsonify(data), status)

    if headers:
        for key, value in headers.items():
            response.headers[key] = value

    return response


def is_json_request() -> bool:
    content_type = request.content_type or ""
    return (
        content_type.split(";", 1)[0].strip().lower()
        == "application/json"
    )


def accepted_format():
    """Choose JSON or XML based on the Accept header."""
    accept = request.headers.get("Accept", "").strip()

    if not accept or accept == "*/*":
        return "json"

    best = request.accept_mimetypes.best_match(
        ["application/json", "application/xml", "text/xml"]
    )

    if best is None or request.accept_mimetypes[best] == 0:
        return None

    return "xml" if best in {"application/xml", "text/xml"} else "json"


def to_xml(value, root_name="response"):
    """Convert JSON-compatible data into XML."""
    from xml.etree.ElementTree import Element, SubElement, tostring

    def append_value(parent, key, item):
        safe_key = re.sub(r"[^A-Za-z0-9_.-]", "_", str(key))

        if not safe_key or (
            not safe_key[0].isalpha() and safe_key[0] != "_"
        ):
            safe_key = f"item_{safe_key}"

        node = SubElement(parent, safe_key)

        if isinstance(item, dict):
            for child_key, child_value in item.items():
                append_value(node, child_key, child_value)
        elif isinstance(item, list):
            for child in item:
                append_value(node, "item", child)
        elif item is None:
            node.text = ""
        else:
            node.text = str(item)

    root = Element(root_name)

    if isinstance(value, dict):
        for key, item in value.items():
            append_value(root, key, item)
    elif isinstance(value, list):
        for item in value:
            append_value(root, "item", item)
    else:
        root.text = str(value)

    return tostring(root, encoding="unicode", xml_declaration=True)


def negotiate_success_response(response):
    """Convert successful JSON responses to XML when requested."""
    if (
        getattr(request, "response_format", "json") == "xml"
        and response.status_code < 400
        and response.mimetype == "application/json"
        and response.get_data()
    ):
        try:
            payload = response.get_json()
            response.set_data(to_xml(payload))
            response.headers["Content-Type"] = (
                "application/xml; charset=utf-8"
            )
        except (ValueError, TypeError):
            return problem(
                500,
                "internal-error",
                "The response could not be serialized.",
            )

    return response


def calculate_etag(order) -> str:
    payload = json.dumps(
        order.as_json(),
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f'"{digest}"'


def require_authorization():
    authorization = request.headers.get("Authorization", "").strip()

    if not authorization:
        return problem(
            401,
            "unauthorized",
            "Authorization header is required.",
        )

    if not authorization.startswith("Bearer "):
        return problem(
            401,
            "unauthorized",
            "Authorization must use Bearer token format.",
        )

    if not authorization[7:].strip():
        return problem(
            401,
            "unauthorized",
            "Bearer token cannot be empty.",
        )

    return None


def check_rate_limit():
    client = request.remote_addr or "unknown"
    now = time.time()
    record = _rate_limits.get(client)

    if record is None or now - float(record["start"]) >= RATE_WINDOW:
        record = {"start": now, "count": 0}
        _rate_limits[client] = record

    record["count"] = int(record["count"]) + 1
    remaining = max(RATE_LIMIT - int(record["count"]), 0)

    if int(record["count"]) > RATE_LIMIT:
        retry_after = max(
            1,
            int(RATE_WINDOW - (now - float(record["start"]))),
        )

        response = problem(
            429,
            "rate-limit-exceeded",
            "Rate limit exceeded.",
        )
        response.headers["Retry-After"] = str(retry_after)
        response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
        response.headers["X-RateLimit-Remaining"] = "0"
        return response

    return {
        "limit": RATE_LIMIT,
        "remaining": remaining,
    }


def options_response_for_path():
    parts = request.path.strip("/").split("/")

    if request.path == "/orders":
        allow = "GET, POST, OPTIONS"
    elif (
        len(parts) == 2
        and parts[0] == "orders"
        and parts[1].isdigit()
    ):
        allow = "GET, PATCH, OPTIONS"
    elif (
        len(parts) == 3
        and parts[0] == "orders"
        and parts[1].isdigit()
        and parts[2] == "cancellation"
    ):
        allow = "POST, OPTIONS"
    else:
        return None

    response = make_response("", 204)
    response.headers["Allow"] = allow
    return response


@app.before_request
def before_request_checks():
    if request.method == "OPTIONS":
        return options_response_for_path()

    response_format = accepted_format()

    if response_format is None:
        return problem(
            406,
            "not-acceptable",
            "Supported response formats are application/json and application/xml.",
        )

    request.response_format = response_format

    if request.path.startswith("/orders"):
        auth_error = require_authorization()

        if auth_error:
            return auth_error

    rate_result = check_rate_limit()

    if hasattr(rate_result, "status_code"):
        return rate_result

    request.rate_limit = rate_result


@app.after_request
def add_response_headers(response):
    response = negotiate_success_response(response)

    if response.status_code not in (204, 304) and response.get_data():
        if response.mimetype == "application/json":
            response.headers["Content-Type"] = (
                "application/json; charset=utf-8"
            )
        elif response.mimetype == "application/problem+json":
            response.headers["Content-Type"] = (
                "application/problem+json; charset=utf-8"
            )
        elif response.mimetype in {"application/xml", "text/xml"}:
            response.headers["Content-Type"] = (
                "application/xml; charset=utf-8"
            )

    rate_info = getattr(request, "rate_limit", None)

    if rate_info:
        response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(
            rate_info["remaining"]
        )

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PATCH, OPTIONS"
    )
    response.headers["Access-Control-Allow-Headers"] = (
        "Content-Type, Accept, Authorization, Idempotency-Key, "
        "If-None-Match, If-Match, X-HTTP-Method-Override"
    )
    response.headers["Access-Control-Expose-Headers"] = (
        "Location, ETag, X-RateLimit-Limit, "
        "X-RateLimit-Remaining, Retry-After"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )

    return response


@app.get("/health")
def health():
    return json_response({
        "service": "orders",
        "status": "alive",
    })


@app.post("/orders")
def create_order():
    if not is_json_request():
        return problem(
            415,
            "unsupported-media-type",
            "Content-Type must be application/json.",
        )

    body = request.get_json(silent=True)

    if body is None:
        return problem(
            400,
            "invalid-request",
            "Request body must be valid JSON.",
        )

    if isinstance(body, dict) and body.get("items") == []:
        return problem(
            422,
            "empty-cart",
            "An order must contain at least one item.",
        )

    errors = validate_place_order(body)

    if errors:
        return problem(
            422,
            "invalid-request",
            "The request body failed validation.",
            errors,
        )

    key = request.headers.get("Idempotency-Key")

    if not key:
        return problem(
            400,
            "invalid-request",
            "Idempotency-Key is required.",
        )

    previous = store.find_by_idempotency_key(key)

    if previous:
        response = json_response(previous.as_json(), 200)
        response.headers["Location"] = f"/orders/{previous.id}"
        response.headers["Cache-Control"] = "no-store"
        return response

    checked_items = []
    total = 0

    try:
        for item in body["items"]:
            catalogue_item = check_item(item["itemId"])
            quantity = item["qty"]

            total += int(round(catalogue_item["price"] * quantity))

            checked_items.append({
                "itemId": catalogue_item["id"],
                "name": catalogue_item["name"],
                "qty": quantity,
                "unitPrice": catalogue_item["price"],
            })

    except ItemUnavailable:
        return problem(
            422,
            "item-unavailable",
            "The requested item is unavailable.",
        )

    except CatalogueItemNotFound:
        return problem(
            422,
            "item-unavailable",
            "The requested catalogue item was not found.",
        )

    except CatalogueRejected:
        return problem(
            400,
            "invalid-request",
            "The catalogue rejected the request.",
        )

    except CatalogueUnavailable:
        response = problem(
            503,
            "catalogue-unavailable",
            "The catalogue service is temporarily unavailable.",
        )
        response.headers["Retry-After"] = "5"
        return response

    try:
        order = store.create_order(
            student_id=body["studentId"],
            items=checked_items,
            delivery_address_id=body["deliveryAddressId"],
            payment_method_id=body["paymentMethodId"],
            total=total,
            status="placed",
            idempotency_key=key,
        )
    except Exception:
        app.logger.exception("Failed to create order")
        return problem(
            500,
            "internal-error",
            "The order could not be created.",
        )

    response = json_response(order.as_json(), 201)
    response.headers["Location"] = f"/orders/{order.id}"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/orders")
def list_orders():
    status = request.args.get("status")

    if status is None:
        orders = store.find_all()
    else:
        if status not in {"placed", "cancelled"}:
            return problem(
                400,
                "invalid-request",
                "Status must be 'placed' or 'cancelled'.",
            )

        orders = store.find_by_status(status)

    response = json_response([
        order.as_json()
        for order in orders
    ])
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    order = store.find_order(order_id)

    if order is None:
        return problem(
            404,
            "order-not-found",
            f"No order {order_id} exists.",
        )

    etag = calculate_etag(order)
    if_none_match = request.headers.get("If-None-Match", "").strip()

    if (
        if_none_match == "*"
        or if_none_match.strip('"') == etag.strip('"')
    ):
        response = make_response("", 304)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "no-store"
        return response

    response = json_response(order.as_json())
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "no-store"
    return response


@app.patch("/orders/<int:order_id>")
def update_order_status(order_id):
    order = store.find_order(order_id)

    if order is None:
        return problem(
            404,
            "order-not-found",
            f"No order {order_id} exists.",
        )

    etag = calculate_etag(order)
    if_match = request.headers.get("If-Match", "").strip()

    if if_match != "*" and if_match.strip('"') != etag.strip('"'):
        return problem(
            412,
            "precondition-failed",
            "The order has changed. Refresh the resource and retry.",
        )

    if not is_json_request():
        return problem(
            415,
            "unsupported-media-type",
            "Content-Type must be application/json.",
        )

    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return problem(
            422,
            "invalid-request",
            "Request body must be a valid JSON object.",
            [{"field": "body", "message": "A JSON object is required."}],
        )

    new_status = body.get("status")

    if new_status not in {"placed", "cancelled"}:
        return problem(
            422,
            "invalid-request",
            "Status must be 'placed' or 'cancelled'.",
            [{"field": "status", "message": "Must be 'placed' or 'cancelled'."}],
        )

    if new_status != order.status and not (
        order.status == "placed" and new_status == "cancelled"
    ):
        return problem(
            409,
            "illegal-transition",
            f"Cannot change order status from '{order.status}' to '{new_status}'.",
        )

    try:
        store.update_order_status(order, new_status)
    except Exception:
        app.logger.exception("Failed to update order status")
        return problem(
            500,
            "internal-error",
            "The order status could not be updated.",
        )

    response = json_response(order.as_json())
    response.headers["ETag"] = calculate_etag(order)
    response.headers["Cache-Control"] = "no-store"
    return response


@app.post("/orders/<int:order_id>")
def method_override(order_id):
    override = request.headers.get(
        "X-HTTP-Method-Override", ""
    ).upper()

    if override == "PATCH":
        return update_order_status(order_id)

    return problem(
        400,
        "invalid-request",
        "Unsupported X-HTTP-Method-Override.",
    )


@app.post("/orders/<int:order_id>/cancellation")
def cancel_order(order_id):
    order = store.find_order(order_id)

    if order is None:
        return problem(
            404,
            "order-not-found",
            f"No order {order_id} exists.",
        )

    if order.status != "placed":
        return problem(
            409,
            "illegal-transition",
            f"Order is already {order.status}.",
        )

    try:
        store.cancel_order(order)
    except Exception:
        app.logger.exception("Failed to cancel order")
        return problem(
            500,
            "internal-error",
            "The order could not be cancelled.",
        )

    response = json_response({
        "orderId": order.id,
        "status": order.status,
    }, 202)
    response.headers["Cache-Control"] = "no-store"
    return response


@app.route("/orders", methods=["OPTIONS"])
def orders_options():
    return options_response_for_path()


@app.route("/orders/<int:order_id>", methods=["OPTIONS"])
def order_options(order_id):
    return options_response_for_path()


@app.route("/orders/<int:order_id>/cancellation", methods=["OPTIONS"])
def cancellation_options(order_id):
    return options_response_for_path()


@app.errorhandler(400)
def bad_request(error):
    return problem(
        400,
        "invalid-request",
        "Malformed request.",
    )


@app.errorhandler(405)
def method_not_allowed(error):
    return problem(
        405,
        "method-not-allowed",
        "HTTP method is not allowed for this resource.",
    )


@app.errorhandler(406)
def not_acceptable(error):
    return problem(
        406,
        "not-acceptable",
        "Requested response format is not supported.",
    )


@app.errorhandler(415)
def unsupported_media_type(error):
    return problem(
        415,
        "unsupported-media-type",
        "Request Content-Type is not supported.",
    )


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error("Unhandled server error: %s", error)
    return problem(
        500,
        "internal-error",
        "An unexpected server error occurred.",
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8082,
        debug=True,
    )
