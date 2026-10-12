# CS543 Assignment 6 — Honest Responses: Status Codes, Errors & Validation

## Team Information

**Team ID:** 02

| Roll No | Name |
|---|---|
| 20251651017 | AMAN KUMAR |
| 20251651090 | SRIKANTA NAYAK |
| 20251651009 | ADITYA VERMA |
| 20251651071 | PRATIK SINHA |

---

## 1. Status Code Map

The Orders Service uses appropriate HTTP status codes to communicate the result of each request.

| Status Code | Meaning | Example |
|---|---|---|
| `200 OK` | Request completed successfully | Reading an order or replaying an idempotent request |
| `201 Created` | A new order was created | `POST /orders` |
| `202 Accepted` | Cancellation was accepted | `POST /orders/{id}/cancellation` |
| `400 Bad Request` | Request syntax or JSON is invalid | Malformed JSON |
| `401 Unauthorized` | Authorization is missing or invalid | Missing Bearer header |
| `404 Not Found` | Requested order does not exist | `GET /orders/9999` |
| `406 Not Acceptable` | Requested response format is unsupported | `Accept: application/pdf` |
| `409 Conflict` | Request conflicts with the current resource state | Cancelling an already-cancelled order |
| `415 Unsupported Media Type` | Request body format is unsupported | Unsupported `Content-Type` |
| `422 Unprocessable Entity` | Request validation or business-rule failure | Empty cart or invalid quantity |
| `429 Too Many Requests` | Rate limit exceeded | Too many requests within the configured window |
| `500 Internal Server Error` | Unexpected server-side failure | Unhandled internal error |
| `503 Service Unavailable` | Required dependency is temporarily unavailable | Catalogue Service unavailable |

A successful order creation returns `201 Created` with a `Location` header, for example:

```http
HTTP/1.1 201 Created
Location: /orders/1
Content-Type: application/json; charset=utf-8
```

The `Location` header identifies the newly created order. A `429` or `503` response should include `Retry-After` so that clients can wait before retrying.

## 2. Problem Details Format and Error Types

The service uses the `problem()` helper in `errors.py` to construct structured error responses. The response content type is:

```http
Content-Type: application/problem+json; charset=utf-8
```

The standard fields are:

- `type`: Stable identifier for the error category.
- `title`: Short description of the error.
- `status`: HTTP status code.
- `detail`: Explanation of the specific failure.
- `errors`: Optional array of field-level validation errors.

The service's error type catalogue includes:

| Error Type | Purpose |
|---|---|
| `empty-cart` | Order has no items |
| `item-unavailable` | Requested menu item is unavailable |
| `payment-declined` | Payment cannot be completed |
| `order-not-found` | Requested order does not exist |
| `illegal-transition` | Requested state transition is invalid |
| `invalid-request` | Request validation failed |
| `catalogue-unavailable` | Catalogue dependency is unavailable |
| `internal-error` | Unexpected server-side failure |

### Observed example: Order not found

Request:

```http
GET /orders/9999
Accept: application/json
Authorization: Bearer test-token
```

Observed response status: `404 Not Found`

```http
Content-Type: application/problem+json; charset=utf-8
```

Observed response body:

```json
{
  "detail": "No order 9999 exists.",
  "status": 404,
  "title": "Order not found",
  "type": "/errors/order-not-found"
}
```

Stable error types help clients distinguish different failures without depending only on the HTTP status code.

## 3. Validation and Multiple Field Errors

The service validates the request before creating an order. If multiple fields are invalid, it returns a single `422 Unprocessable Entity` response containing an `errors` array.

### Example request

The following request has a quantity of zero and omits the delivery address and payment method:

```json
{
  "studentId": 17,
  "items": [
    {
      "itemId": 1,
      "qty": 0
    }
  ]
}
```

### Observed response

Status: `422 Unprocessable Entity`

Content type: `application/problem+json; charset=utf-8`

```json
{
  "detail": "The request body failed validation.",
  "errors": [
    {
      "field": "items[0].qty",
      "message": "must be a positive integer"
    },
    {
      "field": "deliveryAddressId",
      "message": "must be a positive integer"
    },
    {
      "field": "paymentMethodId",
      "message": "must be a positive integer"
    }
  ],
  "status": 422,
  "title": "Invalid request",
  "type": "/errors/invalid-request"
}
```

The client receives all detected validation errors together. This avoids repeated requests just to discover the next invalid field.

### Difference between 400 and 422

- `400 Bad Request` is used for malformed request syntax or invalid JSON.
- `422 Unprocessable Entity` is used when the request can be parsed but fails semantic validation or a business rule.

For example, a quantity of zero is a validation failure and returns `422`.

## 4. Internal Error Handling

Unexpected server errors should be caught by the service's error handler. The client should receive a generic error response rather than a Python traceback, database exception, or internal implementation details.

Example of the intended sanitized response:

```json
{
  "type": "/errors/internal-error",
  "title": "Internal server error",
  "status": 500,
  "detail": "An unexpected server error occurred."
}
```

Detailed diagnostic information should be recorded in server-side logs for debugging. It should not be returned to the client because it may reveal internal paths, database information, or implementation details.

The internal-error response should use `application/problem+json; charset=utf-8`. The exact runtime response should be verified with an intentional test before recording it as an observed result.

## 5. Safe Retries and Retry-After

Clients should decide whether to retry based on the response status and whether the operation may already have changed server state.

| Situation | Safe Retry Strategy |
|---|---|
| A `GET` request fails temporarily | Retry with a bounded delay |
| `POST /orders` times out | Retry using the same `Idempotency-Key` |
| `429 Too Many Requests` | Wait for `Retry-After` before retrying |
| `503 Service Unavailable` | Respect `Retry-After` and use bounded backoff |
| `400 Bad Request` | Correct the request before retrying |
| `422 Unprocessable Entity` | Correct the invalid fields before retrying |
| `404 Not Found` | Verify the resource identifier |
| `409 Conflict` | Resolve the state conflict before retrying |

### Idempotency-Key verification

Order creation was tested with an `Idempotency-Key`.

The first request returned `201 Created`. Repeating the same request with the same key returned `200 OK` with the same order identifier rather than creating another order.

This verifies the tested idempotency behaviour for the repeated request.

The same key should be reused when retrying the same intended order operation. A new key should not be generated for each retry.

### Observed dependency failure

When the Catalogue Service was unavailable, the Orders Service returned:

```http
HTTP/1.1 503 SERVICE UNAVAILABLE
Content-Type: application/problem+json; charset=utf-8
Retry-After: 5
```

Observed body:

```json
{
  "detail": "The catalogue service is temporarily unavailable.",
  "status": 503,
  "title": "Catalogue unavailable",
  "type": "/errors/catalogue-unavailable"
}
```

The client should wait for the indicated interval before retrying.

## 6. Content Negotiation and Response Content-Type

Clients request a response representation using the `Accept` header.

### JSON

```http
Accept: application/json
```

Successful JSON responses use:

```http
Content-Type: application/json; charset=utf-8
```

Problem Details errors use:

```http
Content-Type: application/problem+json; charset=utf-8
```

### XML

The service was tested with:

```http
Accept: application/xml
```

The response returned `200 OK` with:

```http
Content-Type: application/xml; charset=utf-8
```

### Unsupported response format

A request with:

```http
Accept: application/pdf
```

should return `406 Not Acceptable` when the requested representation cannot be produced. The actual response should be recorded in the transcript after verification.

Requests containing JSON should specify:

```http
Content-Type: application/json
```

The service should set an appropriate content type on every response, including errors. Any exceptions, such as a response with no body, should follow the HTTP semantics and the implementation's documented behaviour.

## 7. Dependency Failures and Illegal State Transitions

### Catalogue Service unavailable

When the Catalogue Service was stopped, creating an order returned `503 Service Unavailable` with a `Retry-After: 5` header and a Problem Details response.

This communicates that the failure is temporary and that the client should not retry immediately in a tight loop.

### Illegal state transition

The cancellation endpoint was tested twice for the same order. The first cancellation returned `202 Accepted` with the cancelled status. The second cancellation returned `409 Conflict`.

Observed response body:

```json
{
  "detail": "Order is already cancelled.",
  "status": 409,
  "title": "Illegal state transition",
  "type": "/errors/illegal-transition"
}
```

The `409` response explains that the requested operation conflicts with the order's current state.

## Verification Summary

The following behaviours were observed during development:

- Order creation returned `201 Created`, a `Location` header, and JSON.
- Repeating order creation with the same idempotency key returned the existing order.
- Empty-cart validation returned `422` with Problem Details.
- Invalid quantity and multiple validation errors returned `422` with field-level error objects.
- An unknown order returned `404` with Problem Details.
- Cancelling an already-cancelled order returned `409` with Problem Details.
- Catalogue Service unavailability returned `503` with `Retry-After: 5`.
- XML content negotiation returned an XML content type.
- The Orders Service pytest suite passed after the error-formatting changes.

The following checks must be recorded as verified only after their actual outputs have been captured:

- `429 Too Many Requests` with `Retry-After`.
- Unsupported `Accept` resulting in `406 Not Acceptable`.
- Sanitized `500 Internal Server Error`.
- Timeout and retry behaviour.
- Correct content type on every success and failure response.
- `item-unavailable` and `payment-declined` error triggers, if implemented.

The final submission should include the updated source code, matching `openapi.yaml`, actual curl request/response transcripts, this `NOTES.md`, and the team information.
