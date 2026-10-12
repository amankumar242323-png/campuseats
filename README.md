# CampusEats – Web Services Project

## Team Details

**Group ID:** 02

- Aman Kumar — 20251651017
- Srikanta Nayak — 20251651090
- Aditya Verma — 20251651009
- Pratik Sinha — 20251651071

## Project Overview

CampusEats is a web services project that demonstrates HTTP communication, REST APIs, service integration, SOAP contracts, request validation, API documentation, and error handling.

The project consists of a Flask-based Orders Service and a Catalogue Service. It explores HTTP methods, status codes, request and response headers, API contracts, automated testing, and reliable service communication.

## Assignments

### Assignment 1: HTTP by Hand & Project Setup

- Studied HTTP requests and responses.
- Analysed HTTP methods, headers, status codes, and browser network traffic.
- Documented findings in `http-log.md`, `network-analysis.md`, and `brief.md`.

### Assignment 2: Services, Contracts & Schema

- Designed the service architecture and database schema.
- Created service architecture and schema diagrams.
- Prepared SQL schema documentation.
- Documented the design in `design.pdf` and `schema.sql`.

### Assignment 3: SOAP Payment Partner

- Developed the UniPay Bank Ltd. SOAP payment partner concept.
- Created the WSDL contract.
- Prepared sample SOAP request, response, and fault XML files.

### Assignment 4: REST Orders Service

- Developed a Flask-based Orders Service.
- Integrated the Catalogue Service using HTTP requests.
- Implemented request validation and error handling.
- Worked with timeouts, retries, and idempotency.
- Added automated tests and OpenAPI documentation.

### Assignment 5: Advanced HTTP Features

- Implemented HTTP method handling and OPTIONS responses.
- Added order filtering and method override support.
- Implemented JSON request handling and Bearer header checks.
- Added ETag-based conditional requests using `If-Match` and `If-None-Match`.
- Implemented idempotency keys and rate limiting.
- Added CORS headers, security headers, and gzip compression.
- Documented HTTP exchanges and conceptual answers.

### Assignment 6: Honest Responses — Status Codes, Errors & Validation

- Improved HTTP status codes for successful requests and failures.
- Implemented a shared `problem()` helper for consistent Problem Details responses.
- Used `application/problem+json; charset=utf-8` for error responses.
- Added stable error types, including `empty-cart`, `order-not-found`, `illegal-transition`, and `catalogue-unavailable`.
- Added field-level validation errors using the `errors[]` array and HTTP `422 Unprocessable Content` responses.
- Improved request validation for order items, quantities, and required fields.
- Added safer error handling to avoid exposing internal exception details.
- Implemented JSON and XML response negotiation using the `Accept` header, with `406 Not Acceptable` for unsupported response formats.
- Added `Retry-After` headers to rate-limit and temporary service-unavailability responses.
- Updated `openapi.yaml` to document API responses and Problem Details.
- Added `transcript.txt` with HTTP request and response examples.
- Updated `NOTES.md` with status-code decisions, error handling, validation, and retry safety.
- Verified the Orders Service automated tests: **16 tests passed**.

## Services

| Service | Local URL | Port |
|---|---|---:|
| Catalogue Service | http://127.0.0.1:8081 | 8081 |
| Orders Service | http://127.0.0.1:8082 | 8082 |

## Technologies Used

- **Programming language:** Python
- **Web framework:** Flask
- **Communication:** HTTP and REST APIs
- **Service integration:** HTTP requests between services
- **API documentation:** OpenAPI / YAML
- **Web service contract:** SOAP / WSDL
- **Testing:** pytest and curl
- **Data formats:** JSON and XML
- **Version control:** Git and GitHub

## Running the Project

### 1. Start the Catalogue Service

Open a terminal and run:

```bash
cd catalogue-service
pip install -r requirements.txt
python app.py
```

The Catalogue Service runs at `http://127.0.0.1:8081`.

### 2. Start the Orders Service

Open another terminal and run:

```bash
cd orders-service
pip install -r requirements.txt
python app.py
```

The Orders Service runs at `http://127.0.0.1:8082`.

### 3. Run the Orders Service Tests

Open another terminal:

```bash
cd orders-service
python -m pytest -v
```

The Assignment 6 test run completed successfully with **16 passed**.

### 4. Test the API with curl

Create an order using a valid request body and the required headers:

```bash
curl -i -X POST http://127.0.0.1:8082/orders \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer test-token" \
  -H "Idempotency-Key: order-demo-001" \
  --data-binary "@order-body.json"
```

The request body must match the Orders Service validation rules, and the referenced catalogue item must be available.

## Main Orders Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/orders` | List orders and filter by status |
| POST | `/orders` | Create an order |
| GET | `/orders/{id}` | Retrieve an order |
| PATCH | `/orders/{id}` | Update an order |
| POST | `/orders/{id}/cancellation` | Cancel an order |
| OPTIONS | `/orders` | Discover supported methods |

Refer to `orders-service/openapi.yaml` for the documented API contract, parameters, response formats, and status codes.

## Error Handling and Validation

The Orders Service uses a common Problem Details structure for API errors.

Example:

```json
{
  "type": "/errors/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order 9999 exists."
}
```

Validation failures can include an `errors` array identifying individual fields and their validation messages.

Important status codes include:

| Status Code | Meaning |
|---|---|
| 201 | Order created |
| 400 | Invalid request syntax or malformed input |
| 401 | Unauthorized request |
| 404 | Order not found |
| 409 | Conflict or illegal state transition |
| 412 | Precondition failed |
| 415 | Unsupported request media type |
| 422 | Request validation failed |
| 406 | Unsupported response format |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Temporary service unavailability |

The exact response depends on the endpoint and the failure condition.

## Project Structure

```text
campuseats/
├── catalogue-service/
│   ├── app.py
│   ├── errors.py
│   ├── models.py
│   ├── store.py
│   ├── requirements.txt
│   ├── openapi.yaml
│   ├── NOTES.md
│   └── tests/
├── orders-service/
│   ├── app.py
│   ├── errors.py
│   ├── catalogue_client.py
│   ├── models.py
│   ├── store.py
│   ├── validation.py
│   ├── requirements.txt
│   ├── openapi.yaml
│   ├── NOTES.md
│   ├── transcript.txt
│   └── tests/
├── brief.md
├── design.pdf
├── http-log.md
├── integration.pdf
├── network-analysis.md
├── partner.wsdl
├── schema.sql
├── schema.drawio
├── services.drawio
└── README.md
```

## Limitations

- Order data is stored in memory and may be lost when the service restarts.
- Bearer header validation is demonstrative and does not provide full authentication.
- The project is intended for educational purposes and is not a production-ready ordering platform.

## Conclusion

CampusEats demonstrates practical concepts in HTTP, REST APIs, SOAP contracts, service-to-service communication, API documentation, request validation, consistent error responses, automated testing, and advanced HTTP features. Across six assignments, the project progressively develops a better understanding of web service design and implementation.
