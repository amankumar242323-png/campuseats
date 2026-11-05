# CampusEats – Web Services Project

## Team Details

**Group ID:** 02

- Aman Kumar — 20251651017
- Srikanta Nayak — 20251651090
- Aditya Verma — 20251651009
- Pratik Sinha — 20251651071

## Project Overview

CampusEats is a web services project demonstrating HTTP communication, REST APIs, SOAP contracts, service integration, database connectivity, GraphQL APIs, request validation, API documentation, and error handling.

The project includes a Flask-based Orders Service, a Catalogue Service, and a GraphQL-based Menu/Dishes service connected to MySQL.

## Assignments

### Assignment 1: HTTP by Hand & Project Setup

- Studied HTTP requests and responses.
- Analysed HTTP methods, headers, status codes, and browser network traffic.
- Documented findings in `http-log.md`, `network-analysis.md`, and `brief.md`.

### Assignment 2: Services, Contracts & Schema

- Designed the service architecture and database schema.
- Created architecture and schema diagrams.
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
- Added field-level validation errors using the `errors[]` array and HTTP `422` responses.
- Improved validation for order items, quantities, and required fields.
- Added safer error handling to avoid exposing internal exception details.
- Implemented JSON and XML response negotiation using the `Accept` header.
- Added `Retry-After` headers to rate-limit and temporary service-unavailability responses.
- Updated `orders-service/openapi.yaml`, `transcript.txt`, and `NOTES.md`.
- Verified the Orders Service automated tests: **16 tests passed**.

### Assignment 7: GraphQL Service

- Created a GraphQL API for the CampusEats Menu/Dishes entity using Apollo Server.
- Defined the `Dish` object type, queries, and mutation in `schema.graphql`.
- Connected GraphQL resolvers to MySQL using `mysql2`.
- Created the `campuseats_graphql` database and `dishes` table with sample records.
- Implemented the `dishes` query to list dishes.
- Implemented the `dish(id)` query to retrieve a dish by ID.
- Implemented the `addDish` mutation to insert a new dish into MySQL.
- Developed a plain HTML/CSS frontend that fetches and displays dishes and allows users to add dishes.
- Tested queries and mutations against the database.
- Captured before-and-after screenshots in `graphql-service/screenshots/`.
- **Demo video and screenshots:** [Open Google Drive Folder](https://drive.google.com/drive/folders/1a6bj93E36AmXmM5u7OUYTuO1Yu8kmRgi?usp=sharing).

## Services

| Service | Local URL | Port |
|---|---|---:|
| Catalogue Service | `http://127.0.0.1:8081` | 8081 |
| Orders Service | `http://127.0.0.1:8082` | 8082 |
| GraphQL Menu Service | `http://localhost:4000/` | 4000 |
| GraphQL endpoint | `http://localhost:4000/graphql` | 4000 |

## Technologies Used

- **Programming languages:** Python, JavaScript, SQL
- **Web framework:** Flask, Express
- **GraphQL:** Apollo Server, GraphQL
- **Database:** MySQL
- **Database driver:** `mysql2`
- **Communication:** HTTP, REST APIs, GraphQL, SOAP
- **API documentation:** OpenAPI / YAML, WSDL
- **Testing:** pytest and curl
- **Data formats:** JSON and XML
- **Frontend:** HTML and CSS
- **Version control:** Git and GitHub

## Running the Project

### 1. Start the Catalogue Service

Open a terminal:

```bash
cd catalogue-service
pip install -r requirements.txt
python app.py
```

The Catalogue Service runs at `http://127.0.0.1:8081`.

### 2. Start the Orders Service

Open another terminal:

```bash
cd orders-service
pip install -r requirements.txt
python app.py
```

The Orders Service runs at `http://127.0.0.1:8082`.

### 3. Run Orders Service Tests

```bash
cd orders-service
python -m pytest -v
```

The recorded Assignment 6 test run completed with **16 passed**.

### 4. Start the GraphQL Menu Service

Ensure MySQL is running and the `campuseats_graphql` database has been created using `graphql-service/schema.sql`.

Open a PowerShell terminal:

```powershell
cd graphql-service
$env:DB_PASSWORD = Read-Host "Enter your MySQL root password"
node server.js
```

Enter your MySQL root password when prompted. Keep the terminal running.

Open the frontend at:

`http://localhost:4000/`

The GraphQL endpoint is:

`http://localhost:4000/graphql`

**Security note:** Set the database password through the environment variable. Do not commit passwords or other secrets to GitHub.

## Main Orders Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/orders` | List orders and filter by status |
| POST | `/orders` | Create an order |
| GET | `/orders/{id}` | Retrieve an order |
| PATCH | `/orders/{id}` | Update an order |
| POST | `/orders/{id}/cancellation` | Cancel an order |
| OPTIONS | `/orders` | Discover supported methods |

Refer to `orders-service/openapi.yaml` for the documented API contract and response status codes.

## GraphQL API

The GraphQL service provides the following operations.

### List dishes

```graphql
query {
  dishes {
    id
    name
    price
    available
  }
}
```

### Retrieve a dish by ID

```graphql
query {
  dish(id: 1) {
    id
    name
    price
    available
  }
}
```

### Add a dish

```graphql
mutation {
  addDish(input: { name: "Paneer Roll", price: 90 }) {
    id
    name
    price
    available
  }
}
```

The `dishes` query retrieves all dishes. The `dish` query retrieves a single dish by ID. The `addDish` mutation inserts a dish into the MySQL database.

## Assignment 7: README Questions

### 1. Which CampusEats service did you pick?

We selected the Menu/Dishes service from CampusEats and exposed it through a GraphQL API.

### 2. Name one field a client can skip and one it cannot. Why do we use `!`?

A client can skip `available` in its selection set when it does not need that field. The `name` field is declared as `String!`, meaning it cannot be null in a valid `Dish` result. The `!` symbol marks a field or input as non-null.

### 3. Map the GraphQL operations to SQL.

The `dish(id: ID!)` resolver uses a parameterized SQL query with `WHERE id = ?` to retrieve the requested dish. The `addDish` mutation resolver executes an `INSERT INTO dishes` statement to add a new record.

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

## Project Structure

```text
campuseats/
├── catalogue-service/
├── orders-service/
├── graphql-service/
│   ├── db.js
│   ├── package.json
│   ├── package-lock.json
│   ├── schema.graphql
│   ├── schema.sql
│   ├── server.js
│   ├── public/
│   │   └── index.html
│   └── screenshots/
│       ├── before.png
│       └── after.png
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

- Orders are stored in memory and may be lost when the Orders Service restarts.
- Bearer header validation is demonstrative and does not provide full authentication.
- The GraphQL service requires a running MySQL server and a configured database password.
- The project is intended for educational purposes and is not a production-ready ordering platform.

## Conclusion

Across seven assignments, CampusEats demonstrates practical concepts in HTTP, REST APIs, SOAP contracts, service-to-service communication, database integration, GraphQL queries and mutations, API documentation, request validation, error handling, and automated testing.
## Assignment 8: REST Menu Service

We selected the CampusEats Menu/Catalogue service and implemented it as a REST API using Node.js and Express.

### Routes

| Method | Path | Purpose |
|---|---|---|
| GET | `/items` | Return all menu items (HTTP 200) |
| GET | `/items/:id` | Return one item (HTTP 200) or item-not-found (HTTP 404) |
| POST | `/items` | Create a menu item (HTTP 201) or return validation errors (HTTP 422) |

### README Questions

**1. Which CampusEats service did you pick, and what are its routes?**

We selected the Menu/Catalogue service. Its routes are `GET /items`, `GET /items/:id`, and `POST /items`.

**2. Which status codes did you return, and for which outcomes?**

- `200 OK`: The list or requested item is returned successfully.
- `201 Created`: A new menu item is created successfully.
- `404 Not Found`: The requested item ID does not exist.
- `422 Unprocessable Content`: Required or invalid fields are supplied in the POST body.

**3. Where did you use `req.params` and where `req.body`? Why does POST need `express.json()`?**

`req.params.id` is used in `GET /items/:id` to read the item ID from the URL. `req.body` is used in `POST /items` to read the new item's JSON data. `express.json()` parses incoming JSON request bodies and makes the parsed data available in `req.body`.

### Run Assignment 8

```powershell
cd rest-menu-service
npm install
npm start
```

Open `http://localhost:3000/`.

### Screenshots

- Before POST: `rest-menu-service/screenshots/before.png`
- After POST: `rest-menu-service/screenshots/after.png`

### Demo Video

Add the Google Drive link after uploading the Assignment 8 demonstration video.


### Assignment 8 Demo Video

- **Demo Video:** [Open Google Drive Folder](https://drive.google.com/drive/folders/1GRYleDmb1VKBoqZ4Id442HeF4Ktoca6v?usp=sharing)

