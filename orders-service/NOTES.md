\# CS543 Assignment 5 — HTTP Methods \& Headers



\## Team Information



\*\*Team ID:\*\* 02



| Roll No | Name |

|---|---|

| 20251651017 | AMAN KUMAR |

| 20251651090 | SRIKANTA NAYAK |

| 20251651009 | ADITYA VERMA |

| 20251651071 | PRATIK SINHA |



\---



\# Part A — Methods \& the Message



\## A1. CampusEats Method Map



The following table audits the Orders Service endpoints from Assignment 4 and maps each CampusEats action to the appropriate HTTP method and URL.



| Action | Method | URL | Safe | Idempotent | Reason |

|---|---|---|---|---|---|

| Health check | GET | `/health` | Yes | Yes | Read-only health check |

| Place order | POST | `/orders` | No | No\* | Creates a new order |

| List orders | GET | `/orders` | Yes | Yes | Reads the order collection |

| Filter orders | GET | `/orders?status=placed` | Yes | Yes | Read-only filtered request |

| Read an order | GET | `/orders/{id}` | Yes | Yes | Reads one order |

| Update order status | PATCH | `/orders/{id}` | No | Yes\* | Partially modifies an existing order |

| Cancel order | POST | `/orders/{id}/cancellation` | No | No | Non-CRUD state-changing action |



`\*` `POST /orders` is naturally non-idempotent, but the service makes retries safe using `Idempotency-Key`.



The Orders Service uses resource-oriented URLs. No verb such as `createOrder`, `getOrder`, or `cancelOrder` is used as a top-level URL.



The main resources are:



```text

/orders

/orders/{id}

```



The cancellation action is represented as:



```text

/orders/{id}/cancellation

```



Filtering is represented using a query parameter:



```text

/orders?status=placed

```



\---



\## A2. Model Non-CRUD Actions



Order cancellation is a non-CRUD action because the order is not deleted. Instead, the state of the existing order is changed.



The endpoint is:



```text

POST /orders/{id}/cancellation

```



Example:



```text

POST /orders/1/cancellation

```



A successful cancellation changes the order state from:



```text

placed

```



to:



```text

cancelled

```



The order continues to exist and can still be retrieved using:



```text

GET /orders/1

```



Therefore, cancellation is represented as a POST to a sub-resource instead of using a DELETE operation.



The API does not use a verb-based URL such as:



```text

/cancelOrder

```



\---



\## A3. Safe and Idempotent Classification



An HTTP operation is safe when it does not change server state.



An operation is idempotent when repeating the same request has the same intended effect on server state.



\### Safe Endpoints



The following endpoints are safe:



```text

GET /health

GET /orders

GET /orders?status=placed

GET /orders/{id}

```



They only read information.



\### Idempotent Operations



GET operations are naturally idempotent.



The PATCH order-status operation is designed so that repeating the same update produces the same resulting state.



\### Non-Idempotent Operations



The following POST operations are not naturally idempotent:



```text

POST /orders

POST /orders/{id}/cancellation

```



`POST /orders` creates a new order. Repeating it without protection could create duplicate orders.



The service makes order creation retry-safe using:



```http

Idempotency-Key: order-001

```



The same key identifies retries of the same intended operation.



The first request creates the order and stores the key and result.



A repeated request with the same key returns the original result without creating another order.



Cancellation changes the state of the order and therefore is treated as a state-changing action.



\---



\## A4. Reads Take Query Parameters



The Orders Service uses query parameters for filtering.



Example:



```http

GET /orders?status=placed

```



Another valid example is:



```http

GET /orders?status=cancelled

```



The query parameter is used only to control which resources are returned.



The request remains a pure read operation and therefore continues to use GET.



Invalid status values are rejected with:



```text

400 Bad Request

```



Example:



```http

GET /orders?status=unknown

```



This approach avoids creating separate URLs such as:



```text

/orders/placed

/orders/cancelled

```



\---



\## A5. OPTIONS and Allow



The Orders Service exposes OPTIONS on its resources to advertise the methods supported by each resource.



\### Orders Collection



```http

OPTIONS /orders HTTP/1.1

Host: api.campuseats.app

```



Expected response:



```http

HTTP/1.1 204 No Content

Allow: GET, POST, OPTIONS

```



\### Individual Order



```http

OPTIONS /orders/1 HTTP/1.1

Host: api.campuseats.app

```



Expected response:



```http

HTTP/1.1 204 No Content

Allow: GET, PATCH, OPTIONS

```



\### Cancellation Sub-resource



```http

OPTIONS /orders/1/cancellation HTTP/1.1

Host: api.campuseats.app

```



Expected response:



```http

HTTP/1.1 204 No Content

Allow: POST, OPTIONS

```



\### X-HTTP-Method-Override



For constrained clients that cannot send PATCH directly, the service supports the documented fallback:



```http

X-HTTP-Method-Override: PATCH

```



The override is only a compatibility mechanism. Normal HTTP methods remain the preferred interface.



\---



\## A6. Full HTTP Exchange



\### Create Order Request



```http

POST /orders HTTP/1.1

Host: 127.0.0.1:8082

Content-Type: application/json

Accept: application/json

Authorization: Bearer demo-token

Idempotency-Key: order-001



{

&#x20; "studentId": 17,

&#x20; "items": \[

&#x20;   {

&#x20;     "itemId": 1,

&#x20;     "qty": 2

&#x20;   }

&#x20; ],

&#x20; "deliveryAddressId": 5,

&#x20; "paymentMethodId": 2

}

```



\### Create Order Response



```http

HTTP/1.1 201 Created

Content-Type: application/json

Location: /orders/1

Cache-Control: no-store



{

&#x20; "orderId": 1,

&#x20; "status": "placed",

&#x20; "total": 240,

&#x20; "estimatedMinutes": 30,

&#x20; "createdAt": "2026-09-22T10:00:00+00:00"

}

```



The `Location` header identifies the newly created order resource.



\---



\### Read Order Request



```http

GET /orders/1 HTTP/1.1

Host: 127.0.0.1:8082

Accept: application/json

Authorization: Bearer demo-token

```



\### Read Order Response



```http

HTTP/1.1 200 OK

Content-Type: application/json

Cache-Control: no-store



{

&#x20; "orderId": 1,

&#x20; "status": "placed",

&#x20; "total": 240,

&#x20; "estimatedMinutes": 30,

&#x20; "createdAt": "2026-09-22T10:00:00+00:00"

}

```



\---



\# Part B — Headers on Every Message



\## B1. Content-Type and Negotiation



The Orders Service uses JSON for request and response bodies.



Requests containing JSON use:



```http

Content-Type: application/json

```



Clients can request JSON using:



```http

Accept: application/json

```



Example:



```http

POST /orders HTTP/1.1

Content-Type: application/json

Accept: application/json

```



For an unsupported response format, the service returns:



```text

406 Not Acceptable

```



The API keeps write requests JSON-only to simplify request validation.



For large JSON responses, response compression may be enabled using:



```http

Content-Encoding: gzip

```



\---



\## B2. Correct Status and Location



The Orders Service uses status codes according to the operation.



| Operation | Status |

|---|---|

| Successful read | `200 OK` |

| Successful creation | `201 Created` |

| Accepted cancellation | `202 Accepted` |

| Malformed request | `400 Bad Request` |

| Missing resource | `404 Not Found` |

| State conflict | `409 Conflict` |

| Domain refusal | `422 Unprocessable Entity` |

| Dependency unavailable | `503 Service Unavailable` |



A successful order creation returns:



```http

201 Created

Location: /orders/1

```



The `Location` header identifies the newly created order resource.



\---



\## B3. Authorization



Protected endpoints use:



```http

Authorization: Bearer <token>

```



For example:



```http

Authorization: Bearer demo-token

```



The Authorization header identifies the caller.



A missing or empty Authorization header on a protected endpoint returns:



```text

401 Unauthorized

```



No real authentication/token issuing system is required for this assignment. The focus is on correct HTTP header handling.



Public catalogue browsing does not require authorization, while student-specific order operations are protected.



\---



\## B4. Cache a Read



A single-order GET response uses:



```http

Cache-Control: no-store

```



because order information is user-specific and should not be stored in shared caches.



For a cacheable public catalogue/menu response, the service can use:



```http

Cache-Control: max-age=60

ETag: "menu-v12"

```



The ETag identifies the current representation of the resource.



When the resource changes, the ETag must also change.



\---



\## B5. Rate-Limit Signalling



The API provides rate-limit information using:



```http

X-RateLimit-Limit: 100

X-RateLimit-Remaining: 99

```



The limit is considered per client rather than global.



When the client exceeds its request budget, the API returns:



```text

429 Too Many Requests

```



with:



```http

Retry-After: 60

```



Example:



```http

HTTP/1.1 429 Too Many Requests

X-RateLimit-Limit: 100

X-RateLimit-Remaining: 0

Retry-After: 60

```



The client should wait before retrying.



\---



\## B6. CORS



The Orders Service supports cross-origin browser requests using CORS response headers.



Example:



```http

Access-Control-Allow-Origin: \*

```



For preflight requests, the OPTIONS response can include:



```http

Access-Control-Allow-Origin: \*

Access-Control-Allow-Methods: GET, POST, PATCH, OPTIONS

Access-Control-Allow-Headers: Content-Type, Accept, Authorization, Idempotency-Key, If-Match

```



This allows a browser application running on another origin to call the API when the request satisfies the configured CORS policy.



\---



\## B7. Security and General Headers



The service uses the following security-related headers:



```http

X-Content-Type-Options: nosniff

Strict-Transport-Security: max-age=31536000; includeSubDomains

```



`X-Content-Type-Options: nosniff` prevents browsers from MIME-sniffing the response away from the declared content type.



`Strict-Transport-Security` instructs compatible browsers to use HTTPS for future requests.



In production, the service is expected to be served over HTTPS.



The framework may also provide standard headers such as:



```http

Date

Server

```



\---



\# Part C — Caching and Safe Retries



\## C1. Conditional GET — 304 Not Modified



A cacheable resource can be requested using the ETag previously returned by the server.



Example initial response:



```http

HTTP/1.1 200 OK

Content-Type: application/json

Cache-Control: max-age=60

ETag: "menu-v12"

```



The client stores:



```text

"menu-v12"

```



A later request can use:



```http

GET /restaurants/9/menu HTTP/1.1

Host: api.campuseats.app

Accept: application/json

If-None-Match: "menu-v12"

```



If the menu has not changed, the server returns:



```http

HTTP/1.1 304 Not Modified

ETag: "menu-v12"

```



No response body is sent.



The client uses its cached representation.



This saves bandwidth because the complete menu does not need to be downloaded again.



\---



\## C2. Conditional Write — 412 Precondition Failed



The Orders Service uses `If-Match` for protected updates.



A client first reads the current representation and receives an ETag:



```http

ETag: "order-v5"

```



The client then sends:



```http

PATCH /orders/1 HTTP/1.1

Host: api.campuseats.app

Content-Type: application/json

Accept: application/json

Authorization: Bearer demo-token

If-Match: "order-v5"



{

&#x20; "status": "cancelled"

}

```



If the order is still version `v5`, the update can proceed.



If another client has already changed the order and the current ETag is different, the server returns:



```http

HTTP/1.1 412 Precondition Failed

```



This prevents one editor from silently overwriting another editor's changes.



\---



\## C3. Idempotency-Key



Order creation uses:



```http

Idempotency-Key: order-001

```



The same key must be reused for every retry of the same intended operation.



First request:



```text

POST /orders

Idempotency-Key: order-001

```



The service:



1\. Validates the request.

2\. Checks whether the key already exists.

3\. If it is new, creates the order.

4\. Stores the key with the order.

5\. Returns the created order.



If the same key is received again:



```text

POST /orders

Idempotency-Key: order-001

```



the service returns the original order instead of performing the creation again.



This prevents duplicate orders when a client does not receive the first response and retries.



A duplicate order would cause real business damage because the student could receive multiple orders or be charged multiple times.



\---



\## C4. Safe-Retry Plan



| Risky Operation | Method | Safety Mechanism | Why |

|---|---|---|---|

| Place order | POST `/orders` | `Idempotency-Key` | Prevents duplicate order creation |

| Read menu | GET `/restaurants/{id}/menu` | `If-None-Match` | Saves bandwidth using cached representation |

| Update order | PATCH `/orders/{id}` | `If-Match` | Prevents lost updates |

| Cancel order | POST `/orders/{id}/cancellation` | State validation | Prevents invalid repeated cancellation |



\### Summary



```text

POST create operation

&#x20;       |

&#x20;       v

Idempotency-Key

&#x20;       |

&#x20;       v

Safe retry without duplicate creation

```



```text

GET cacheable resource

&#x20;       |

&#x20;       v

If-None-Match

&#x20;       |

&#x20;       v

304 Not Modified

```



```text

PATCH update

&#x20;       |

&#x20;       v

If-Match

&#x20;       |

&#x20;       v

412 Precondition Failed if resource changed

```



\---



\# Part D — Verify and Document



\## D1. curl -v Transcript



The final `curl-transcript.txt` will contain verbose HTTP exchanges for:



1\. Successful order creation returning `201 Created` and `Location`.

2\. Repeated order creation using the same `Idempotency-Key`.

3\. Conditional GET returning `304 Not Modified`.

4\. Conditional write rejected with `412 Precondition Failed`.

5\. Invalid request returning `400 Bad Request`.

6\. Missing order returning `404 Not Found`.

7\. Missing/invalid authorization returning `401 Unauthorized`.



The transcript will be generated using:



```text

curl -v

```



so that request and response headers are visible.



\---



\## D2. Headers Table



| Endpoint | Request Headers | Response Headers |

|---|---|---|

| `POST /orders` | Content-Type, Accept, Authorization, Idempotency-Key | Content-Type, Location, Cache-Control, rate-limit headers |

| `GET /orders` | Accept, Authorization | Content-Type, Cache-Control, rate-limit headers |

| `GET /orders/{id}` | Accept, Authorization, If-None-Match | Content-Type, ETag, Cache-Control |

| `PATCH /orders/{id}` | Content-Type, Accept, Authorization, If-Match | Content-Type, ETag |

| `POST /orders/{id}/cancellation` | Content-Type, Accept, Authorization | Content-Type, rate-limit headers |

| `OPTIONS /orders` | Origin, Access-Control-Request-Method, Access-Control-Request-Headers | Allow, Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers |



\---



\# NOTES Questions



\## 1. For three of your endpoints, give the method, the success status, and the single response header that matters most — and why.



\### Endpoint 1 — Create Order



```text

POST /orders

```



Success:



```text

201 Created

```



Most important response header:



```http

Location: /orders/1

```



The Location header tells the client where the newly created order resource can be retrieved.



\### Endpoint 2 — Read Order



```text

GET /orders/{id}

```



Success:



```text

200 OK

```



Most important response header:



```http

ETag: "order-v5"

```



The ETag identifies the current representation and can be used for conditional requests.



\### Endpoint 3 — Cancel Order



```text

POST /orders/{id}/cancellation

```



Success:



```text

202 Accepted

```



Most important response header:



```http

Content-Type: application/json

```



It identifies the format of the JSON response body returned to the client.



\---



\## 2. Which of your endpoints are safe, and which are idempotent? Which one is neither, and how did you make it retry-safe?



\### Safe endpoints



The safe endpoints are:



```text

GET /health

GET /orders

GET /orders?status=placed

GET /orders/{id}

```



They only read information.



\### Idempotent endpoints



GET operations are naturally idempotent.



The PATCH status update is designed to be idempotent when the same target state is submitted.



\### Neither



The main endpoint that is neither safe nor naturally idempotent is:



```text

POST /orders

```



Creating an order changes state and repeating the request could create another order.



It is made retry-safe with:



```http

Idempotency-Key: order-001

```



The server stores the key and original result. A repeated request with the same key returns the stored result instead of performing the creation again.



\---



\## 3. Show one ETag from your service, the request that returns 304, and the write that returns 412. What does each save or prevent?



Example ETag:



```http

ETag: "menu-v12"

```



Conditional GET:



```http

GET /restaurants/9/menu HTTP/1.1

Host: api.campuseats.app

Accept: application/json

If-None-Match: "menu-v12"

```



Response when unchanged:



```http

HTTP/1.1 304 Not Modified

ETag: "menu-v12"

```



The `304 Not Modified` response saves bandwidth because the cached menu can be reused.



For a conditional write:



```http

PATCH /orders/1 HTTP/1.1

Host: api.campuseats.app

Content-Type: application/json

Accept: application/json

Authorization: Bearer demo-token

If-Match: "order-v5"



{

&#x20; "status": "cancelled"

}

```



If the current ETag no longer matches:



```http

HTTP/1.1 412 Precondition Failed

```



The `412` prevents a stale client from overwriting a newer update made by another client.



\---



\## 4. You return 422 for one case and 400 for another. Give the exact request that triggers each, and explain the difference.



\### 422 — Domain Refusal



Example:



```http

POST /orders HTTP/1.1

Host: 127.0.0.1:8082

Content-Type: application/json

Accept: application/json

Authorization: Bearer demo-token

Idempotency-Key: order-422



{

&#x20; "studentId": 17,

&#x20; "items": \[

&#x20;   {

&#x20;     "itemId": 1,

&#x20;     "qty": 2

&#x20;   }

&#x20; ],

&#x20; "deliveryAddressId": 5,

&#x20; "paymentMethodId": 2

}

```



If item `1` exists but is unavailable, the request is structurally valid but cannot be fulfilled.



The service returns:



```text

422 Unprocessable Entity

```



\### 400 — Invalid Request



Example:



```http

POST /orders HTTP/1.1

Host: 127.0.0.1:8082

Content-Type: application/json

Accept: application/json

Authorization: Bearer demo-token

Idempotency-Key: order-400



{

&#x20; "studentId": "17",

&#x20; "items": \[],

&#x20; "deliveryAddressId": 5,

&#x20; "paymentMethodId": 2

}

```



The request has invalid input types and an empty items list.



The service returns:



```text

400 Bad Request

```



\### Difference



`400` means the request itself is malformed or invalid.



`422` means the request is structurally valid, but the requested business operation cannot be fulfilled.



\---



\## 5. A browser page on another origin calls your API and is blocked — yet your server logs show a 200. Who blocked it, and which response header fixes it?



The browser enforced the same-origin policy and blocked the browser page from accessing the response.



The server can still log:



```text

200 OK

```



because the server successfully processed the request.



The relevant response header is:



```http

Access-Control-Allow-Origin: \*

```



For a restricted production origin, the header can specify the allowed origin instead of `\*`.



CORS response headers tell the browser which cross-origin requests are permitted.



\---



\## 6. Name one response where you set Cache-Control to allow caching and one where you must use no-store. Why each?



\### Cacheable response



A public catalogue/menu response can use:



```http

Cache-Control: max-age=60

ETag: "menu-v12"

```



The menu can be cached temporarily because it is public read-only information.



\### No-store response



A user-specific order response can use:



```http

Cache-Control: no-store

```



because order information is user-specific and should not be stored in shared caches.



\---



\## 7. Your search endpoint is a GET. When would POST be the right choice instead, and what do you give up by switching?



GET is appropriate for normal search and filtering because the operation is a read and the query can be represented using the URL.



POST would be appropriate when the search request is too complex to represent safely or conveniently in the query string, for example when the search contains a large structured JSON filter.



For example:



```http

POST /orders/search

Content-Type: application/json



{

&#x20; "statuses": \["placed", "cancelled"],

&#x20; "restaurants": \[1, 2, 3],

&#x20; "minTotal": 100,

&#x20; "maxTotal": 1000

}

```



By switching from GET to POST, the operation loses some benefits associated with GET, including normal URL-based caching, easy bookmarking, and direct representation of the search criteria in the URL.



Therefore, GET remains preferred for simple read filters.



\---



\## 8. Location appears on a 201 and on a 3xx. What does it point to in each case?



For a successful resource creation:



```http

HTTP/1.1 201 Created

Location: /orders/42

```



the Location header points to the newly created resource.



For a redirect such as:



```http

HTTP/1.1 3xx

Location: https://api.campuseats.app/orders/42

```



the Location header identifies the target URL to which the client should redirect or continue the request according to the specific 3xx status code.



Therefore:



```text

201 + Location

→ newly created resource



3xx + Location

→ redirect target

```



\---



\# Assignment 5 Implementation Checklist



\## Part A



\- \[x] A1 Method audit

\- \[x] A2 Non-CRUD action

\- \[x] A3 Safe and idempotent classification

\- \[x] A4 Query parameters

\- \[x] A5 OPTIONS and Allow design

\- \[x] A6 Full HTTP exchange



\## Part B



\- \[x] B1 Content-Type and Accept

\- \[x] B2 Correct status codes and Location

\- \[x] B3 Authorization

\- \[x] B4 Cache-Control and ETag

\- \[x] B5 Rate-limit signalling

\- \[x] B6 CORS

\- \[x] B7 Security headers



\## Part C



\- \[x] C1 If-None-Match and 304

\- \[x] C2 If-Match and 412

\- \[x] C3 Idempotency-Key

\- \[x] C4 Safe-retry plan



\## Part D



\- \[x] D1 curl -v transcript requirements

\- \[x] D2 Headers table

\- \[x] D3 NOTES questions



\---



\# Final Verification Requirements



Before submission, the following must be verified:



```text

1\. All Orders Service endpoints use the correct HTTP methods.

2\. OPTIONS returns an Allow header.

3\. Content-Type and Accept are handled.

4\. Authorization is checked on protected endpoints.

5\. 201 responses include Location.

6\. Cache-Control and ETag are implemented where required.

7\. If-None-Match can produce 304.

8\. If-Match can produce 412.

9\. Idempotency-Key prevents duplicate order creation.

10\. Rate-limit headers are returned.

11\. 429 includes Retry-After.

12\. CORS headers are returned.

13\. Security headers are returned.

14\. curl -v transcript contains all required success and failure cases.

15\. OpenAPI reflects the updated methods, statuses and headers.

16\. All tests pass.

```



\---





