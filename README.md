# CampusEats – Web Services Project

## Team Details
**Group ID:** 02

- Aman Kumar — 20251651017
- Srikanta Nayak — 20251651090
- Aditya Verma — 20251651009
- Pratik Sinha — 20251651071

## Project Overview
CampusEats is a web services project that demonstrates HTTP communication, REST APIs, service integration, SOAP contracts, request validation, and error handling.

## Assignments

### Assignment 1: HTTP by Hand & Project Setup
- Studied HTTP requests and responses.
- Analysed methods, headers, status codes, and browser network traffic.
- Documented findings in `http-log.md`, `network-analysis.md`, and `brief.md`.

### Assignment 2: Services, Contracts & Schema
- Designed the service architecture and database schema.
- Created diagrams and SQL schema documentation.
- Documented the design in `design.pdf` and `schema.sql`.

### Assignment 3: SOAP Payment Partner
- Integrated the UniPay Bank Ltd. SOAP payment partner concept.
- Created the WSDL contract and sample SOAP request, response, and fault XML files.

### Assignment 4: REST Orders Service
- Developed a Flask-based Orders Service.
- Integrated the Catalogue Service using HTTP requests.
- Implemented validation, error handling, timeouts, retries, and idempotency.
- Added automated tests and OpenAPI documentation.

### Assignment 5: Advanced HTTP Features
- Implemented HTTP method handling and OPTIONS responses.
- Added order filtering and method override support.
- Implemented JSON content negotiation and Bearer header checks.
- Added ETag-based conditional requests.
- Implemented idempotency keys and rate limiting.
- Added CORS, security headers, and gzip compression.
- Documented HTTP exchanges and conceptual answers.

## Services

| Service | Local URL | Port |
|---|---|---|
| Catalogue Service | http://127.0.0.1:8081 | 8081 |
| Orders Service | http://127.0.0.1:8082 | 8082 |

## Running the Project

### 1. Start Catalogue Service
```bash
cd catalogue-service
pip install -r requirements.txt
python app.py
```

### 2. Start Orders Service
Open another terminal:

```bash
cd orders-service
pip install -r requirements.txt
python app.py
```

### 3. Run Tests
From the appropriate service directory:

```bash
pytest -v
```

## Main Orders Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/orders` | List orders and filter by status |
| POST | `/orders` | Create an order |
| GET | `/orders/<id>` | Retrieve an order |
| PATCH | `/orders/<id>` | Update an order |
| POST | `/orders/<id>/cancellation` | Cancel an order |
| OPTIONS | `/orders` | Discover supported methods |

## Project Structure

```text
campuseats/
├── catalogue-service/
├── orders-service/
├── http-log.md
├── network-analysis.md
├── brief.md
├── design.pdf
├── schema.sql
├── partner.wsdl
├── curl-transcript.txt
├── NOTES.md
└── README.md
```

## Limitations
- Order data is stored in memory and may be lost when the service restarts.
- Bearer header validation is demonstrative and does not provide full authentication.
- The project is intended for educational purposes.

## Conclusion
CampusEats demonstrates practical concepts of HTTP, REST, SOAP, service-to-service communication, API contracts, testing, and advanced HTTP features.
