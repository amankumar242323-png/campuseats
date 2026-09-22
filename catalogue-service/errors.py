from flask import jsonify


TITLES = {
    "invalid-request": "Invalid request",
    "item-not-found": "Menu item not found",
    "restaurant-not-found": "Restaurant not found",
    "state-conflict": "State conflict",
    "domain-rejected": "Domain rule rejected",
    "dependency-unavailable": "Dependency unavailable"
}


def problem(
    status,
    code,
    detail="",
    errors=None
):

    body = {
        "type": f"/errors/{code}",
        "title": TITLES[code],
        "status": status,
        "detail": detail
    }

    if errors:
        body["errors"] = errors

    return jsonify(body), status