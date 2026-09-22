# CS543 — Assignment 4

# Rebuilding CampusEats Catalogue Service in REST

## Team

Group ID: \_\_\_\_\_\_\_\_\_\_

Members:

1. Aman Kumar — 20251651017
2. Pratik Sinha — 20251651071
3. Aditya Verma — 20251651009
4. Shrikanta Nayak — 20251651090



# Part A — Model the Service

## A1 — Selected Service

Selected service:

Catalogue Service

The Catalogue Service was selected because it is one of the CampusEats
services defined in Assignment 2 and was not implemented as the Payments
service in Tutorial 4.

The existing service boundary is preserved.

The Catalogue Service owns restaurants, menus and food-item information.



## A2 — Operations Originally Expressed as SOAP

The operations that could have been written as SOAP operations are:

* addMenuItem(...)
* itemDetails(...)
* searchFood(...)
* getMenu(...)
* checkItems(...)



## A3 — REST Nouns

The durable resources are:

* menu items
* restaurant menus
* availability

The SOAP-style verbs do not appear as verbs in the URL paths.



## A4 — Resource Table

|Method|URL|What it does|Success|Failure|
|-|-|-|-|-|
|POST|/menu-items|Create a menu item|201|400, 422|
|GET|/menu-items/{id}|Read one menu item|200|404|
|GET|/menu-items?search=text|Search food items|200|400|
|GET|/restaurants/{id}/menu|Read restaurant menu|200|404|
|PATCH|/menu-items/{id}/availability|Change availability|200|400, 404, 409|



## A5 — Hard Choice

The least comfortable SOAP operation to map to REST was setAvailability().

A verb-based URL such as /menu-items/1/setAvailability was rejected because
the assignment requires resource-oriented URLs and the operation verb should
not become the URL.

The chosen design is PATCH /menu-items/{id}/availability. The URL identifies
the availability state of a menu item and PATCH expresses a partial state
change.

This keeps the operation's meaning while following REST resource modelling.



# Part B — OpenAPI

The OpenAPI contract is written before the implementation code.

openapi.yaml contains:

* info
* servers
* paths
* components.schemas

Schemas are defined once and reused through $ref.

All declared failure responses are documented.



# Part C — Implementation

The service follows the Tutorial 4 structure:

* models.py
* store.py
* errors.py
* app.py
* tests/

The storage is an in-process dictionary.

No other service imports the Catalogue Service store.



## Record versus Representation

The MenuItem class stores internal fields such as idempotency\_key and
created\_at.

The as\_json() method exposes only the public representation.

The idempotency key is therefore never leaked through the API response.



## Validation

validate\_menu\_item() validates POST /menu-items before application code
accesses request fields.

validate\_availability() performs validation for the availability update.

This replaces the XML Schema validation that was available in the SOAP
implementation.



## Status Codes

201 — menu item successfully created.

200 — successful read, search or availability update.

400 — malformed request.

404 — requested menu item or restaurant does not exist.

409 — requested state is already the current state.

422 — request is valid but violates a domain rule.



## Idempotency

POST /menu-items requires Idempotency-Key.

The key is stored with the created menu item.

If the same key is received again, the original representation is returned
with 200 and no second menu item is created.



# Part D — Network Resilience

The Catalogue Service makes an HTTP request to another CampusEats service.

The Orders service address is obtained through the ORDERS\_URL environment
variable rather than being hard-coded.

The outbound call uses a two-second timeout.

Temporary failures are retried up to three times using exponential backoff
with jitter.

4xx responses are never retried.

The Catalogue Service uses graceful degradation when the Orders dependency
is unavailable because catalogue creation does not require Orders to be
available. The catalogue record is still created and the dependency
notification failure does not cause the catalogue request itself to fail.



# Assignment 3 Comparison



## 1\. WSDL versus OpenAPI

The Assignment 3 WSDL declared XML Schema types, SOAP messages, operations,
SOAP binding and the service/port endpoint.

The Assignment 4 OpenAPI contract represents the same contract information
using schemas, request/response bodies, HTTP paths and methods, and server
URLs.

The difference in line count is mainly caused by the different way the two
contract formats express the same information.

Two WSDL elements that disappear as independent declarations are:

1. SOAP binding.
2. WSDL service/port.

The HTTP URL and HTTP method already communicate the protocol and destination
in the REST design.



## 2\. SOAP Fault Mapping

The Assignment 3 SOAP payment work contained structured SOAP faults.

For the REST service, failures are represented using HTTP status codes and
the common Problem JSON representation.

Example:

HTTP 404 Not Found

{
"type": "/errors/item-not-found",
"title": "Menu item not found",
"status": 404,
"detail": "No menu item 999"
}

Returning an application error inside HTTP 200 would be a problem because
the network infrastructure, monitoring systems, caches and clients interpret
the HTTP status as the basic success/failure result.



## 3\. UDDI Publish / Find / Bind

In the older setup, UDDI conceptually provided publish, find and bind.

In the new setup, publish and find are handled by the deployment/platform
and service name resolution.

The explicit bind step disappears because the REST service is directly
called over HTTP once its URL has been resolved.



## 4\. XML Schema versus validate()

The XML Schema responsibility from Assignment 3 is now carried by:

validate\_menu\_item()

and

validate\_availability()

For example, without validation a request missing the price field could
reach the implementation and cause incorrect behaviour or a runtime error.



## 5\. Where SOAP Would Still Be Preferred

SOAP would still be appropriate at an enterprise boundary where an external
partner requires SOAP and where strong message-level security and established
enterprise WS-\* guarantees are required.

For the internal CampusEats Catalogue Service, REST is simpler because the
service primarily exposes resource-oriented data and state changes.



# Testing

The following evidence will be added after execution:

1. OpenAPI validator output showing zero errors.
2. pytest output showing four passing tests.
3. curl -i successful create.
4. curl -i repeated request using the same Idempotency-Key.
5. curl -i malformed request.
6. curl -i unknown resource.
7. curl -i state conflict.

