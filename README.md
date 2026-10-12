# CampusEats
**Course:** CS543  
**Group ID:** 02
## Group Members
1. **AMAN KUMAR** — 20251651017
2. **SRIKANTA NAYAK** — 20251651090
3. **ADITYA VERMA** — 20251651009
4. **PRATIK SINHA** — 20251651071
---
# Project Overview
CampusEats is a campus food-service system developed as part of the CS543 Web Services course.
The system is designed around multiple independent services with clear service boundaries and data ownership. Students can discover food items, place orders, and manage their orders, while the system communicates with other services such as the Catalogue Service and Payment Service.
The project is developed incrementally through multiple assignments covering HTTP fundamentals, service-oriented architecture, API contracts, database design, external SOAP integration, REST API design, service-to-service communication, error handling, idempotency, retries, and automated testing.
## Main Services
- **Identity Service**
- **Catalogue Service**
- **Order Service**
- **Payment Service**
---
# Assignment 1 — HTTP by Hand & Project Setup
Assignment 1 focuses on understanding HTTP communication, analyzing browser network requests, setting up the Git repository, and preparing the initial CampusEats system brief.
## Tasks Completed
1. HTTP requests using `curl`
2. HTTP request and response analysis
3. Browser Network analysis
4. Git repository setup
5. CampusEats system brief
## Assignment 1 Files
- `http-log.md` — Five HTTP request/response experiments using `curl.exe`.
- `network-analysis.md` — Analysis of website requests using Chrome DevTools Network panel.
- `brief.md` — CampusEats system brief describing the system, users, nouns, and operations.
---
# Assignment 2 — Services, Contracts & Schema
Assignment 2 focuses on identifying service boundaries, defining service capabilities, specifying service operations, designing the main `placeOrder` operation, and preparing the database schema.
## Services
The CampusEats system is divided into four main services.
### 1. Identity Service
Responsible for:
- Users
- Roles
- Identity-related information
### 2. Catalogue Service
Responsible for:
- Restaurants
- Menus
- Food items
- Food availability
- Food search
### 3. Order Service
Responsible for:
- Orders
- Order items
- Order status
- Order tracking
- Order cancellation
### 4. Payment Service
Responsible for:
- Payments
- Payment creation
- Payment status
---
## Data Ownership
| Service | Data Owned |
|---|---|
| Identity Service | Users, Roles |
| Catalogue Service | Restaurants, Menus, Food Items |
| Order Service | Orders, Order Items |
| Payment Service | Payments |
---
## Catalogue Operations
- `checkItems`
- `itemDetails`
- `searchFood`
- `getMenu`
## Order Operations
- `placeOrder`
- `cancelOrder`
- `getOrder`
- `trackOrder`
- `updateOrderStatus`
## Payment Operations
- `createPayment`
- `getPaymentStatus`
---
# Place Order Operation
The main Order Service operation defined in Assignment 2 is:
```text
placeOrder
```
### Inputs
The operation accepts:
- Customer information
- Requested food items
- Payment details
### Output
```text
Order Result
```
### Possible Errors
- `CustomerNotFound`
- `ItemNotFound`
- `ItemUnavailable`
- `InvalidQuantity`
- `InvalidOrder`
- `PaymentFailed`
- `OrderCreationFailed`
---
## Assignment 2 Files
- `design.pdf` — Complete service and database design document.
- `services.drawio` — Editable service design diagram.
- `services.png` — Exported service design diagram.
- `schema.drawio` — Editable database ER diagram.
- `schema.png` — Exported database ER diagram.
- `schema.sql` — Database `CREATE TABLE` statements.
---
# Assignment 3 — Integrate an External SOAP Partner
Assignment 3 focuses on integrating CampusEats with an external SOAP-based payment partner.
For this assignment, **UniPay Bank Ltd.** is used as the external payment partner.
The external payment operation is:
```text
charge
```
The communication uses SOAP over HTTPS.
## External Partner
**Partner:** UniPay Bank Ltd.  
**Operation:** `charge`  
**Protocol:** SOAP over HTTPS  
**Endpoint:**
```text
https://api.unipay.example/pay
```
---
## Assignment 3 Tasks Completed
1. External partner selection
2. Partner WSDL design
3. SOAP request design
4. SOAP response design
5. SOAP fault design
6. HTTP binding
7. Service discovery
8. Fault mapping
---
## Assignment 3 Files
- `integration.pdf` — Complete Assignment 3 integration documentation.
- `partner.wsdl` — WSDL contract for the external SOAP partner.
- `soap-request.xml` — SOAP `charge` request.
- `soap-response.xml` — Successful SOAP response.
- `soap-fault.xml` — SOAP fault for a declined card.
---
# SOAP Integration Flow
```text
CampusEats Orders
        |
        | SOAP / HTTPS
        | charge
        v
UniPay Bank
        |
        +------> chargeResponse
        |
        +------> SOAP Fault
        |
        v
CampusEats Orders
```
The SOAP integration demonstrates how CampusEats can communicate with an external payment partner while keeping the internal services separated from the partner-specific protocol.
---
# Assignment 4 — Rebuilding a CampusEats Service in REST
Assignment 4 focuses on rebuilding one of the previously defined CampusEats services using REST principles.
For this assignment, the **Orders Service** was selected.
The service follows the service boundary and data ownership established in Assignment 2 and communicates with the Catalogue Service through HTTP.
## Technologies Used
- **Python**
- **Flask**
- **Requests**
- **Pytest**
- **OpenAPI 3.0.3**
---
# Orders Service
The Orders Service is responsible for creating and managing food orders.
The service owns the order data and exposes REST APIs for creating, retrieving, filtering, and cancelling orders.
The service also validates order requests and checks the requested food items with the Catalogue Service before creating an order.
---
# Orders Service Structure
```text
orders-service/
│
├── .gitignore
├── app.py
├── catalogue_client.py
├── errors.py
├── models.py
├── openapi.yaml
├── requirements.txt
├── store.py
├── validation.py
│
└── tests/
    └── test_orders.py
```
---
# REST Resource Design
The Orders Service uses resource-oriented URLs.
The main collection is:
```text
/orders
```
An individual order is represented as:
```text
/orders/{id}
```
Cancellation is represented as a state-changing sub-resource:
```text
/orders/{id}/cancellation
```
Filtering is handled using query parameters:
```text
/orders?status=placed
```
The API does not use verbs such as `createOrder` or `cancelOrder` in the URL.
---
# REST Endpoint Summary
| Method | URL | Purpose | Success | Main Failures |
|---|---|---|---|---|
| GET | `/health` | Service health check | `200` | — |
| OPTIONS | `/orders` | Show supported collection methods | `204` | — |
| POST | `/orders` | Create an order | `201` / `200` | `400`, `401`, `406`, `422`, `429`, `503` |
| GET | `/orders` | List/filter orders | `200` | `400`, `401`, `406`, `429` |
| OPTIONS | `/orders/{id}` | Show supported order methods | `204` | — |
| GET | `/orders/{id}` | Retrieve one order | `200` / `304` | `401`, `404`, `406`, `429` |
| PATCH | `/orders/{id}` | Update order status with `If-Match` | `200` | `400`, `401`, `404`, `406`, `412`, `429` |
| POST | `/orders/{id}` | PATCH fallback using `X-HTTP-Method-Override` | `200` | `400`, `401`, `404`, `406`, `412`, `429` |
| OPTIONS | `/orders/{id}/cancellation` | Show cancellation methods | `204` | — |
| POST | `/orders/{id}/cancellation` | Cancel an order | `202` | `401`, `404`, `406`, `409`, `429` |
---
# 1. Health Check
```http
GET /health
```
Checks whether the Orders Service is running.
### Response
```text
200 OK
```
### Example
```json
{
  "service": "orders",
  "status": "alive"
}
```
---
# 2. Create Order
```http
POST /orders
```
Creates a new order.
## Required Headers
Protected Orders endpoints require an authorization header:
```http
Authorization: Bearer demo-token
```
Order creation also requires an idempotency key:
```http
Idempotency-Key: order-001
```
## Request Body
```json
{
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
```
## Successful Response
```text
201 Created
```
The response contains a `Location` header.
Example:
```text
Location: /orders/1
```
Example response body:
```json
{
  "orderId": 1,
  "status": "placed",
  "total": 240,
  "estimatedMinutes": 30,
  "createdAt": "2026-09-22T10:00:00+00:00"
}
```
---
# 3. Idempotent Order Creation
The Orders Service supports the `Idempotency-Key` HTTP header for safe retries of order creation.
Example:
```http
POST /orders
Idempotency-Key: order-001
```
When the same request is sent again with the same idempotency key, the service returns the already-created order instead of creating another order.
### First Request
```text
201 Created
```
### Repeated Request
```text
200 OK
```
Both responses refer to the same order.
This prevents duplicate orders when a client retries a request because of a network timeout or temporary failure.
---
# 4. Get One Order
```http
GET /orders/{id}
```
Retrieves one order using its order ID.
### Successful Response
```text
200 OK
```
### Unknown Order
```text
404 Not Found
```
Example:
```http
GET /orders/999
```
Example error response:
```json
{
  "detail": "No order 999",
  "status": 404,
  "title": "Order not found",
  "type": "/errors/order-not-found"
}
```
---
# 4a. Conditional GET with ETag
Single-order reads return an `ETag` header.
```http
GET /orders/1
Authorization: Bearer demo-token
```
The client can send the same ETag back with `If-None-Match`:
```http
If-None-Match: "etag-value"
```
If the order representation has not changed, the service returns:
```text
304 Not Modified
```
No response body is returned for `304`.
---
# 5. List Orders
```http
GET /orders
```
Returns all currently stored orders.
### Response
```text
200 OK
```
Example:
```json
[
  {
    "orderId": 1,
    "status": "placed",
    "total": 240,
    "estimatedMinutes": 30,
    "createdAt": "2026-09-22T10:00:00+00:00"
  }
]
```
---
# 6. Filter Orders
Orders can be filtered using the `status` query parameter.
```http
GET /orders?status=placed
```
Supported values:
```text
placed
cancelled
```
### Valid Request
```text
200 OK
```
### Invalid Status
```text
400 Bad Request
```
Example:
```http
GET /orders?status=abc
```
---
# 6a. Update Order Status
```http
PATCH /orders/{id}
```
Updates an order status. The request must include the current ETag in `If-Match` to prevent stale writes.
Required headers:
```http
Authorization: Bearer demo-token
Content-Type: application/json
If-Match: "etag-value"
```
Request body:
```json
{
  "status": "cancelled"
}
```
Successful response:
```text
200 OK
```
If the ETag does not match the current order representation, the service returns:
```text
412 Precondition Failed
```
For clients that cannot send `PATCH`, the service also supports:
```http
POST /orders/{id}
X-HTTP-Method-Override: PATCH
```
---
# 6b. OPTIONS and Allow
The Orders Service exposes `OPTIONS` for method discovery.
| Request | Allow |
|---|---|
| `OPTIONS /orders` | `GET, POST, OPTIONS` |
| `OPTIONS /orders/{id}` | `GET, PATCH, OPTIONS` |
| `OPTIONS /orders/{id}/cancellation` | `POST, OPTIONS` |
Each successful `OPTIONS` response returns:
```text
204 No Content
```
---
# 7. Cancel an Order
```http
POST /orders/{id}/cancellation
```
Requests cancellation of an existing order.
### Successful Cancellation
```text
202 Accepted
```
Example response:
```json
{
  "orderId": 1,
  "status": "cancelled"
}
```
### Order Not Found
```text
404 Not Found
```
### State Conflict
If the order is already cancelled or is otherwise not in a cancellable state:
```text
409 Conflict
```
This prevents invalid state transitions.
---
# Request Validation
Request validation is implemented separately in:
```text
validation.py
```
The main validation function is:
```python
validate_place_order(body)
```
The service validates the complete request before using its fields.
The following fields are validated:
- `studentId`
- `items`
- `itemId`
- `qty`
- `deliveryAddressId`
- `paymentMethodId`
For each item:
- `itemId` must be an integer.
- `qty` must be a positive integer.
The `items` list must contain at least one item.
---
# Example Invalid Request
```json
{
  "studentId": "17",
  "items": [],
  "deliveryAddressId": 5,
  "paymentMethodId": 2
}
```
The service returns:
```text
400 Bad Request
```
Example error response:
```json
{
  "detail": "The request body is invalid.",
  "errors": [
    [
      "studentId",
      "required integer"
    ],
    [
      "items",
      "must be a non-empty list"
    ]
  ],
  "status": 400,
  "title": "Invalid request",
  "type": "/errors/invalid-request"
}
```
---
# Error Handling
The Orders Service uses one consistent error format.
The helper is implemented in:
```text
errors.py
```
The main function is:
```python
problem(status, code, detail, errors=None)
```
The returned error structure contains:
```json
{
  "type": "/errors/...",
  "title": "...",
  "status": 400,
  "detail": "..."
}
```
Validation errors can additionally contain an `errors` field.
---
# HTTP Status Codes
The API uses meaningful HTTP status codes.
| Status Code | Meaning |
|---|---|
| `200 OK` | Successful read or idempotent repeat |
| `201 Created` | New order created |
| `202 Accepted` | State-changing cancellation accepted |
| `204 No Content` | Successful `OPTIONS` response |
| `304 Not Modified` | Conditional GET matched the current ETag |
| `400 Bad Request` | Malformed or invalid request |
| `401 Unauthorized` | Missing or invalid bearer authorization header |
| `404 Not Found` | Requested order does not exist |
| `406 Not Acceptable` | Requested response format is not supported |
| `409 Conflict` | Current order state does not allow the operation |
| `412 Precondition Failed` | `If-Match` did not match the current ETag |
| `422 Unprocessable Entity` | Domain-level refusal such as unavailable item |
| `429 Too Many Requests` | Client exceeded the in-memory request limit |
| `503 Service Unavailable` | Catalogue dependency unavailable |
---
# Order Model
The order data model is implemented in:
```text
models.py
```
The Order model stores:
- Order ID
- Student ID
- Items
- Delivery address ID
- Payment method ID
- Total
- Status
- Idempotency key
- Creation timestamp
Example internal model:
```text
Order
 ├── id
 ├── student_id
 ├── items
 ├── delivery_address_id
 ├── payment_method_id
 ├── total
 ├── status
 ├── idempotency_key
 └── created_at
```
---
# Public Order Representation
The internal Order object and its API representation are intentionally different.
The public response is generated using:
```python
as_json()
```
The public response contains:
- `orderId`
- `status`
- `total`
- `estimatedMinutes`
- `createdAt`
Internal fields such as:
```text
student_id
delivery_address_id
payment_method_id
idempotency_key
```
are not exposed directly in the public representation.
This keeps internal information separate from the API response.
---
# In-Memory Store
For the current implementation, the Orders Service uses an in-memory store.
The implementation is in:
```text
store.py
```
The store maintains:
```text
_orders
_idempotency_keys
_next_id
```
The store supports:
- Creating orders
- Finding an order by ID
- Finding orders by status
- Finding orders by idempotency key
- Cancelling an order
- Updating order status
- Returning all orders
This design keeps the service simple for development and demonstration.
The current implementation is not intended to provide persistent storage across service restarts.
---
# Catalogue Service Integration
The Orders Service communicates with the Catalogue Service when creating an order.
The integration is implemented in:
```text
catalogue_client.py
```
The Orders Service sends a request to the Catalogue Service for each requested menu item.
The expected Catalogue Service endpoint is:
```text
GET /menu-items/{id}
```
The Catalogue Service provides information such as:
```json
{
  "id": 1,
  "restaurantId": 1,
  "menuId": 1,
  "name": "Veg Burger",
  "description": "Fresh vegetable burger",
  "price": 120.0,
  "available": true
}
```
The Orders Service uses the returned price and availability information while constructing the order.
---
# Service-to-Service Communication
The Catalogue Service URL is configured using an environment variable:
```text
CATALOGUE_URL
```
Default local value:
```text
http://127.0.0.1:8081
```
Example:
```powershell
Env: Catalogue URL="http://127.0.0.1:8081"
```
The Orders Service does not directly access the Catalogue Service's internal data store.
Communication happens through HTTP APIs.
This maintains the service boundary defined in Assignment 2.
---
# Timeout and Retry Handling
The Orders Service uses a dedicated client for communication with the Catalogue Service.
The client supports:
- Request timeout
- Multiple attempts
- Exponential backoff
- Random jitter
- Handling of HTTP 5xx failures
- Handling of network failures
Default configuration:
```text
CATALOGUE_TIMEOUT=2.0
CATALOGUE_MAX_ATTEMPTS=3
CATALOGUE_BASE_DELAY=0.5
```
These settings can be overridden through environment variables.
---
# Retry Strategy
The retry delay follows exponential backoff.
The delay is based on:
```text
base_delay × 2^attempt
```
A small random jitter is added to reduce the possibility of multiple clients retrying at exactly the same time.
The implementation retries:
- Network failures
- Timeouts
- Server-side `5xx` responses
The implementation does not retry normal client-side `4xx` responses.
Examples:
```text
Attempt 1
   |
   | failure
   v
wait + jitter
   |
Attempt 2
   |
   | failure
   v
wait + jitter
   |
Attempt 3
```
---
# Dependency Failure Handling
If the Catalogue Service remains unavailable after all retry attempts, the Orders Service returns:
```text
503 Service Unavailable
```
Example:
```json
{
  "detail": "Catalogue service is unavailable after all retry attempts.",
  "status": 503,
  "title": "Catalogue unavailable",
  "type": "/errors/catalogue-unavailable"
}
```
This prevents a downstream Catalogue Service failure from being returned as an unexplained internal error.
---
# Catalogue Failure Scenarios
The Orders Service handles the following Catalogue outcomes.
## Item Not Found
If the requested menu item does not exist, the order is rejected.
```text
422 Unprocessable Entity
```
## Item Unavailable
If a menu item exists but is unavailable:
```text
422 Unprocessable Entity
```
## Catalogue Rejects Request
A client-side Catalogue error is treated as an invalid request:
```text
400 Bad Request
```
## Catalogue Service Unavailable
If the Catalogue Service cannot be reached after retries:
```text
503 Service Unavailable
```
---
# OpenAPI Specification
The Orders Service API is documented using:
```text
openapi.yaml
```
The specification uses:
```text
OpenAPI 3.0.3
```
The OpenAPI document includes:
- API information
- Servers
- Paths
- HTTP methods
- Request bodies
- Parameters
- Responses
- Error schema
- Order schema
- Order item schema
- Cancellation result schema
---
# OpenAPI Servers
The specification contains local and deployed API server definitions.
Example:
```text
http://localhost:8082
```
and:
```text
https://api.campuseats.dev
```
---
# OpenAPI Schemas
The following schemas are defined under:
```text
components:
  schemas:
```
### PlaceOrderRequest
Represents the request body for creating an order.
### OrderItemRequest
Represents one item in the order.
### Order
Represents the public Order API response.
### CancellationResult
Represents the cancellation response.
### Problem
Represents the common API error structure.
The schemas are defined once and referenced using `$ref`.
---
# OpenAPI Validation
The OpenAPI specification was validated using:
```text
openapi-spec-validator
```
Validation result:
```text
orders-service/openapi.yaml: OK
```
This confirms that the current OpenAPI specification passes the validator without errors.
---
# Automated Testing
Automated tests are implemented using:
```text
pytest
```
Test file:
```text
orders-service/tests/test_orders.py
```
The Assignment 4 tests cover the major required scenarios.
## Test 1 — Create Order
Checks that:
- The order is created successfully.
- Response status is `201`.
- `Location` header is present.
- Correct order ID is returned.
## Test 2 — Idempotency
Checks that:
- The first request creates the order.
- Repeating the same request with the same idempotency key returns `200`.
- The same order ID is returned.
- The Catalogue check is not repeated.
## Test 3 — Invalid Request
Checks that invalid input returns:
```text
400 Bad Request
```
and uses the expected problem response structure.
## Test 4 — Unknown Order
Checks that requesting an unknown order returns:
```text
404 Not Found
```
with the expected problem response structure.
---
# Test Execution
From the Orders Service directory:
```powershell
cd orders-service
python -m pytest -q
```
Current test result:
```text
....                                                                     [100%]
4 passed
```
All four implemented Orders Service tests pass.
---
# End-to-End Communication Flow
The overall order creation flow is:
```text
Client
  |
  | POST /orders
  | Idempotency-Key
  v
Orders Service
  |
  | Validate Request
  v
Request Validation
  |
  | Valid
  v
Check Idempotency Key
  |
  | New Key
  v
Catalogue Service
  |
  | GET /menu-items/{id}
  v
Validate Item
  |
  +---------> Item Not Found
  |
  +---------> Item Unavailable
  |
  +---------> Catalogue Unavailable
  |
  v
Calculate Order Total
  |
  v
Create Order
  |
  v
201 Created
  |
  +----> Location: /orders/{id}
```
---
# Order Cancellation Flow
```text
Client
  |
  | POST /orders/{id}/cancellation
  v
Orders Service
  |
  | Find Order
  |
  +----> Not Found ------> 404
  |
  v
Check Current Status
  |
  +----> Cannot Cancel --> 409
  |
  v
Update Status
  |
  v
202 Accepted
```
---
# Error Flow
The service converts different failure conditions into appropriate HTTP responses.
```text
Invalid Request
      |
      v
400 Bad Request
Missing Order
      |
      v
404 Not Found
Unavailable Item
      |
      v
422 Unprocessable Entity
Invalid State
      |
      v
409 Conflict
Catalogue Unavailable
      |
      v
503 Service Unavailable
```
---
# Example API Usage
## Start Catalogue Service
From the Catalogue Service directory:
```powershell
python app.py
```
The Catalogue Service runs on:
```text
http://127.0.0.1:8081
```
---
## Start Orders Service
From the Orders Service directory:
```powershell
python app.py
```
The Orders Service runs on:
```text
http://127.0.0.1:8082
```
---
# Health Check
```powershell
curl.exe -i http://127.0.0.1:8082/health
```
Expected response:
```text
HTTP/1.1 200 OK
```
Example body:
```json
{
  "service": "orders",
  "status": "alive"
}
```
---
# Create Order Example
```powershell
curl.exe -i -X POST http://127.0.0.1:8082/orders `
  -H "Content-Type: application/json" `
  -H "Idempotency-Key: order-001" `
  -d "{\"studentId\":17,\"items\":[{\\"itemId\\":1,\\"qty\\":2}],\"deliveryAddressId\":5,\"paymentMethodId\":2}"
```
Expected response:
```text
HTTP/1.1 201 CREATED
Location: /orders/1
```
---
# Repeat the Same Order
Using the same idempotency key:
```powershell
curl.exe -i -X POST http://127.0.0.1:8082/orders `
  -H "Content-Type: application/json" `
  -H "Idempotency-Key: order-001" `
  -d "{\"studentId\":17,\"items\":[{\\"itemId\\":1,\\"qty\\":2}],\"deliveryAddressId\":5,\"paymentMethodId\":2}"
```
Expected response:
```text
HTTP/1.1 200 OK
```
The same order ID is returned.
---
# Get Order
```powershell
curl.exe -i http://127.0.0.1:8082/orders/1
```
Expected response:
```text
HTTP/1.1 200 OK
```
---
# Filter Orders
```powershell
curl.exe -i "http://127.0.0.1:8082/orders?status=placed"
```
Expected response:
```text
HTTP/1.1 200 OK
```
---
# Cancel Order
```powershell
curl.exe -i -X POST http://127.0.0.1:8082/orders/1/cancellation
```
Expected response:
```text
HTTP/1.1 202 ACCEPTED
```
---
# Repeated Cancellation
Trying to cancel the same order again:
```powershell
curl.exe -i -X POST http://127.0.0.1:8082/orders/1/cancellation
```
Expected response:
```text
HTTP/1.1 409 CONFLICT
```
---
# Unknown Order
```powershell
curl.exe -i http://127.0.0.1:8082/orders/999
```
Expected response:
```text
HTTP/1.1 404 NOT FOUND
```
---
# Invalid Request
Example:
```json
{
  "studentId": "17",
  "items": [],
  "deliveryAddressId": 5,
  "paymentMethodId": 2
}
```
Expected response:
```text
HTTP/1.1 400 BAD REQUEST
```
---
# Project-Level Architecture
The current CampusEats project can be represented as:
```text
                         CampusEats
                             |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
 Identity Service     Catalogue Service      Orders Service
                                                   |
                                                   |
                                                   v
                                            Catalogue Service
                                                   |
                                                   v
                                            Payment Service
                                                   |
                                                   v
                                             External Partner
                                             UniPay Bank SOAP
```
The actual service interaction is controlled through service APIs rather than directly accessing another service's internal data.
---
# Repository Structure
The repository contains Assignment 1, Assignment 2, Assignment 3, and the working service implementations.
```text
campuseats/
│
├── body.json
├── brief.md
├── design.pdf
├── http-log.md
├── integration.pdf
├── network-analysis.md
├── partner.wsdl
├── README.md
├── schema.drawio
├── schema.sql
├── services.drawio
├── soap-fault.xml
├── soap-request.xml
├── soap-response.xml
│
├── catalogue-service/
│   ├── app.py
│   ├── availability.json
│   ├── bad-body.json
│   ├── body.json
│   ├── curl-transcript.txt
│   ├── errors.py
│   ├── models.py
│   ├── NOTES.md
│   ├── openapi.yaml
│   ├── requirements.txt
│   ├── store.py
│   └── tests/
│       └── test_catalogue.py
│
└── orders-service/
    ├── .gitignore
    ├── app.py
    ├── catalogue_client.py
    ├── errors.py
    ├── models.py
    ├── openapi.yaml
    ├── requirements.txt
    ├── store.py
    ├── validation.py
    └── tests/
        └── test_orders.py
```
---
# Service Ports
For local development:
| Service | Port |
|---|---:|
| Catalogue Service | `8081` |
| Orders Service | `8082` |
Local URLs:
```text
Catalogue Service
http://127.0.0.1:8081
Orders Service
http://127.0.0.1:8082
```
---
# Environment Configuration
The Orders Service supports configuration through environment variables.
## Catalogue URL
```text
CATALOGUE_URL
```
Default:
```text
http://127.0.0.1:8081
```
## Catalogue Timeout
```text
CATALOGUE_TIMEOUT
```
Default:
```text
2.0
```
## Maximum Attempts
```text
CATALOGUE_MAX_ATTEMPTS
```
Default:
```text
3
```
## Base Retry Delay
```text
CATALOGUE_BASE_DELAY
```
Default:
```text
0.5
```
## Orders Rate Limit
```text
RATE_LIMIT
```
Default:
```text
100
```
---
# Installation
Install the dependencies for the Orders Service using:
```powershell
cd orders-service
pip install -r requirements.txt
```
The requirements include:
```text
Flask
Requests
Pytest
```
---
# Running the Project
## Step 1 — Start Catalogue Service
```powershell
cd catalogue-service
python app.py
```
Catalogue Service:
```text
http://127.0.0.1:8081
```
## Step 2 — Start Orders Service
Open another terminal:
```powershell
cd orders-service
python app.py
```
Orders Service:
```text
http://127.0.0.1:8082
```
## Step 3 — Test the Health Endpoint
```powershell
curl.exe -i http://127.0.0.1:8082/health
```
---
# Design Decisions
## REST Resource Naming
The API uses nouns instead of verbs.
Example:
```text
/orders
```
instead of:
```text
/createOrder
```
and:
```text
/orders/{id}/cancellation
```
for cancellation.
---
## HTTP Methods
The service uses HTTP methods according to the operation:
```text
GET  -> Read
POST -> Create / State-changing action
```
Filtering is implemented using query parameters:
```text
GET /orders?status=placed
```
---
## Idempotency
Order creation uses:
```text
Idempotency-Key
```
This prevents duplicate order creation when the client repeats the same request.
The key is stored together with the created order.
---
## Error Representation
All API errors use the same problem structure.
Example:
```json
{
  "type": "/errors/order-not-found",
  "title": "Order not found",
  "status": 404,
  "detail": "No order 999"
}
```
This makes error handling consistent for clients.
---
# REST and SOAP Comparison in CampusEats
The project demonstrates both REST and SOAP communication.
## REST
Used for internal CampusEats service communication.
Characteristics:
- HTTP resources
- HTTP methods
- JSON representations
- HTTP status codes
- OpenAPI contract
- Query parameters
## SOAP
Used for the external UniPay Bank integration.
Characteristics:
- SOAP envelope
- XML messages
- WSDL contract
- SOAP Fault
- SOAP over HTTPS
The two approaches demonstrate how different communication styles can coexist in a service-oriented system.
---
# Assignment 4 Implementation Highlights
The Orders Service implements the main concepts required for the REST rebuilding task:
## REST API
The service exposes resource-oriented endpoints for orders.
## OpenAPI
The complete API contract is defined in:
```text
orders-service/openapi.yaml
```
## Request Validation
Incoming requests are validated before processing.
## Consistent Errors
All failures use a common problem response structure.
## Idempotency
Repeated requests using the same idempotency key return the existing order instead of creating a duplicate.
## Service-to-Service HTTP Call
The Orders Service calls the Catalogue Service using HTTP.
## Timeout
Catalogue requests have a configurable timeout.
## Retry
Temporary network and server failures are retried.
## Exponential Backoff and Jitter
Retries use increasing delays with a random jitter.
## Automated Testing
Four core pytest tests cover creation, idempotency, validation failure, and missing-resource handling.
---
**---
Assignment 5 — HTTP Methods, Headers, Caching, and Safe Retries
Assignment 5 extends the Orders Service from Assignment 4 by implementing additional HTTP protocol behavior. The focus is on method discovery, request and response headers, content negotiation, conditional requests, rate limiting, browser security, compression, and reliable retries.
Assignment 5 Objectives
- Define and verify the HTTP methods supported by each resource.
- Return OPTIONS responses with the correct Allow header.
- Support order filtering using query parameters.
- Support method override for clients that cannot send PATCH.
- Validate JSON request and response media types.
- Return appropriate errors for unsupported response formats.
- Use ETag, If-None-Match, and If-Match for conditional requests.
- Use Idempotency-Key to avoid duplicate order creation during retries.
- Apply rate limiting and return Retry-After when the limit is exceeded.
- Configure CORS and security-related response headers.
- Support gzip compression where applicable.
- Record request/response experiments in the curl transcript and document the design decisions.
HTTP Method Map
Resource	Method	Purpose
/health	GET	Check service health
/orders	GET	List orders and filter by status
/orders	POST	Create an order
/orders	OPTIONS	Discover supported collection methods
/orders/{id}	GET	Retrieve one order
/orders/{id}	PATCH	Update an order
/orders/{id}	POST	Support PATCH through method override
/orders/{id}	OPTIONS	Discover supported order methods
/orders/{id}/cancellation	POST	Request order cancellation
/orders/{id}/cancellation	OPTIONS	Discover cancellation methods


OPTIONS and Allow
The service exposes OPTIONS so clients can discover the methods supported by each resource.
Request	Expected Allow header
OPTIONS /orders	GET, POST, OPTIONS
OPTIONS /orders/{id}	GET, PATCH, OPTIONS
OPTIONS /orders/{id}/cancellation	POST, OPTIONS


Successful OPTIONS requests return 204 No Content.
Filtering and Method Override
Orders can be filtered by status:
GET /orders?status=placed
The supported status filters are placed and cancelled. An unsupported status, such as status=abc, returns 400 Bad Request.
For clients that cannot send PATCH, the service supports method override:
POST /orders/1
X-HTTP-Method-Override: PATCH
Content-Type: application/json
The override header allows the request to be handled as a PATCH operation, subject to normal validation and precondition checks.
Content Negotiation and Request Validation
The service checks request and response media-type requirements. JSON requests should use:
Content-Type: application/json
Clients can request JSON using:
Accept: application/json
Malformed or invalid request data returns 400 Bad Request. If the requested response representation is unsupported, the service returns 406 Not Acceptable. Domain-level failures, such as an unavailable menu item, are represented using the appropriate application error response.
Conditional Requests with ETag
A GET /orders/{id} response includes an ETag validator. Clients can send that value in a later request:
GET /orders/1
If-None-Match: "etag-value"
If the representation has not changed, the service returns 304 Not Modified without a response body.
For updates, clients send the current validator in If-Match:
PATCH /orders/1
If-Match: "etag-value"
Content-Type: application/json
If the supplied validator does not match the current representation, the service returns 412 Precondition Failed. This prevents updates based on stale data.
Idempotency and Safe Retries
Order creation uses the Idempotency-Key request header. A first successful request creates an order and returns 201 Created. Repeating the same request with the same key returns the existing order rather than creating a duplicate; the repeat returns 200 OK.
This mechanism is useful when a client cannot tell whether a request succeeded because of a network timeout.
Authorization Header Check
Protected Orders endpoints check for a Bearer authorization header, for example:
Authorization: Bearer demo-token
Implementation limitation: the current demonstration checks the Bearer header format/presence; it does not implement full token verification or production-grade authentication. The example token is a local placeholder.
Rate Limiting
The service includes an in-memory request limit. When a client exceeds the configured limit, the service returns:
HTTP/1.1 429 Too Many Requests
Retry-After: 30
The Retry-After header tells the client when it should try again. Because the limiter is in memory, its state is not shared across multiple service instances and may reset when the process restarts.
CORS and Security Headers
The service configures Cross-Origin Resource Sharing (CORS) headers for browser-based clients. The allowed request headers include headers needed by the API, such as Content-Type, Accept, Authorization, Idempotency-Key, If-None-Match, If-Match, and X-HTTP-Method-Override.
The response also includes security-related headers:
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
HSTS is intended for HTTPS deployments. For a production deployment, the header should only be used when the service is served over HTTPS and the domain configuration is appropriate.
Gzip Compression
The service supports gzip compression for applicable responses when the client advertises gzip support using Accept-Encoding. The client can inspect the response headers to verify whether compression was applied.
Error and Status Code Summary
Status	Meaning in the Orders Service
200 OK	Successful read, update, or idempotent repeat
201 Created	New order created
202 Accepted	Cancellation request accepted
204 No Content	Successful OPTIONS response
304 Not Modified	Conditional GET indicates no change
400 Bad Request	Invalid request or unsupported filter value
401 Unauthorized	Required Bearer header missing or malformed
404 Not Found	Requested order does not exist
406 Not Acceptable	Requested response format is unsupported
409 Conflict	Requested state transition is not allowed
412 Precondition Failed	If-Match condition failed
422 Unprocessable Entity	Domain-level validation/refusal
429 Too Many Requests	Request limit exceeded
503 Service Unavailable	Catalogue dependency unavailable after retries


Assignment 5 Files
The Assignment 5 work is documented and tested in the Orders Service. Relevant files include:
- orders-service/app.py — HTTP routes, headers, conditional requests, rate limiting, CORS, compression, and related behavior.
- orders-service/store.py — in-memory order storage and idempotency support.
- orders-service/tests/test_orders.py — automated API tests.
- orders-service/NOTES.md — conceptual answers and implementation notes.
- orders-service/curl-transcript.txt — recorded HTTP request/response experiments.
Verification
The following behavior was checked during development:
Scenario	Expected result
Filter orders using status=placed	200 OK with matching orders
OPTIONS /orders	204 No Content and Allow header
OPTIONS /orders/{id}	204 No Content and Allow header
OPTIONS /orders/{id}/cancellation	204 No Content and Allow header
Matching If-None-Match	304 Not Modified, no response body
Non-matching If-Match on update	412 Precondition Failed
Invalid request	400 Bad Request
Unknown order	404 Not Found
Missing/malformed Bearer header	401 Unauthorized
Automated Orders Service tests	4 tests passed in the recorded run


Run the automated tests from the repository root:
cd orders-service
python -m pytest -v
The recorded test suite contains four core tests covering order creation, idempotency, invalid requests, and unknown orders. Manual HTTP experiments are additionally recorded in curl-transcript.txt.
Assignment 5 Limitations
- Order data, idempotency keys, and rate-limit state are held in memory.
- The Bearer header check is not full authentication or token validation.
- A production deployment should use persistent storage, real authentication, HTTPS, and a shared rate-limiting mechanism where multiple instances are deployed.
- HTTP behavior should be re-tested against the final code and environment before claiming that every manual scenario passes.
**---
# Current Verification Status
The current Orders Service implementation has been manually and automatically checked.
Verified scenarios include:
```text
Orders Service health        -> 200
Catalogue Service health     -> 200
Create order                 -> 201
Location header              -> Present
Idempotent repeat            -> 200
Get existing order           -> 200
List/filter orders           -> 200
Invalid status               -> 400
Malformed order request      -> 400
Unknown order                -> 404
First cancellation           -> 202
Repeated cancellation        -> 409
Catalogue unavailable        -> 503
OpenAPI validation            -> OK
Pytest                        -> 4 passed
```
---
# Current Limitations
The current service implementation uses in-memory storage.
Therefore, order data is lost when the Orders Service restarts.
The current implementation is intended for service/API development and demonstration.
For a production deployment, persistent database storage should be used.
---
# Future Development
The CampusEats system can be extended with the following features:
- PostgreSQL-based persistent storage for Orders Service
- Authentication and authorization
- JWT-based user authentication
- Complete Payment Service implementation
- Real payment gateway integration
- Restaurant and menu management
- Order tracking
- Delivery Service
- Notification Service
- Centralized logging
- API gateway
- Service discovery
- Containerized deployment
- Docker Compose for local orchestration
- Production monitoring and observability
---
# Learning Outcomes
Through this project, the following concepts were implemented and demonstrated:
- HTTP request/response model
- REST resource design
- HTTP methods
- HTTP status codes
- Service boundaries
- Data ownership
- API contracts
- OpenAPI
- SOAP
- WSDL
- SOAP Faults
- Service-to-service communication
- Request validation
- Error handling
- Idempotency
- Timeout handling
- Retry mechanisms
- Exponential backoff
- Jitter
- Automated API testing
- Git-based project management
---
# Conclusion
CampusEats demonstrates the evolution of a service-oriented application from basic HTTP communication to independently designed services and API-based integration.
Assignment 1 established the HTTP and project foundations.
Assignment 2 defined the CampusEats service boundaries, operations, data ownership, and database design.
Assignment 3 demonstrated integration with an external SOAP payment partner using WSDL, SOAP messages, and SOAP Fault handling.
Assignment 4 extended the project with a REST-based Orders Service using Flask, OpenAPI, request validation, consistent problem responses, idempotency, service-to-service communication, timeout and retry handling, and automated tests.
Assignment 5 further develops the service's HTTP behavior through method discovery, content negotiation, conditional requests, safe retries, rate limiting, CORS, security headers, and response compression.
The resulting project provides a foundation for further development into a complete campus food ordering platform.
---