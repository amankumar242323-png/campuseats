# CampusEats

**Course:** CS543  
**Group ID:** 02

## Group Members

1. **AMAN KUMAR** — 20251651017
2. **SRIKANTA NAYAK** — 20251651090
3. **ADITYA VERMA** — 20251651009
4. **PRATIK SINHA** — 20251651071

---

## Project Overview

CampusEats is a campus food-service system project for CS543.

This repository contains the practical work related to HTTP requests, browser network analysis, Git, the CampusEats system brief, service-oriented system design, service contracts, database schema design, and integration with an external SOAP partner.

---

# Assignment 1 — HTTP by Hand & Project Setup

Assignment 1 focuses on understanding HTTP communication, analyzing browser network requests, setting up a Git repository, and defining the CampusEats system.

## Tasks Completed

1. HTTP requests using curl
2. Browser Network analysis
3. Git repository setup
4. CampusEats system brief

## Assignment 1 Files

- `http-log.md` — Five HTTP request/response experiments using `curl.exe`.
- `network-analysis.md` — Analysis of website requests using Chrome DevTools Network panel.
- `brief.md` — CampusEats system brief describing what, who, nouns, and verbs.

---

# Assignment 2 — Services, Contracts & Schema

Assignment 2 focuses on designing the CampusEats services, defining service contracts, specifying the central `placeOrder` operation, designing the database schema, and validating service boundaries.

## Services

The CampusEats system is divided into four services:

- **Identity Service** — Responsible for identity and user-related data.
- **Order Service** — Responsible for orders and order-related data.
- **Catalogue Service** — Responsible for restaurants, menus, and food items.
- **Payment Service** — Responsible for payments and payment status.

Each service has its own data ownership boundary and defined service contract.

## Tasks Completed

1. Capability identification
2. Service design
3. Service contracts
4. `placeOrder` full specification
5. Database schema design
6. Service validation

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

For this assignment, **UniPay Bank** is used as the external payment partner. The `charge` operation is integrated using SOAP over HTTPS, while the internal CampusEats services remain REST-based.

## External SOAP Partner

**Partner:** UniPay Bank Ltd.  
**Operation:** `charge`  
**Protocol:** SOAP over HTTPS  
**Endpoint:** `https://api.unipay.example/pay`

The integration includes a WSDL contract, SOAP request and response messages, a SOAP fault, HTTP binding, service discovery, and fault mapping into the CampusEats `placeOrder` contract.

## Assignment 3 Tasks Completed

1. Context and external partner selection
2. Partner WSDL design
3. SOAP request, response, and fault messages
4. HTTP binding
5. Service discovery and registry entry
6. Fault mapping

## Assignment 3 Files

- `integration.pdf` — Complete Assignment 3 integration documentation.
- `partner.wsdl` — Editable WSDL contract for the external SOAP partner.
- `soap-request.xml` — SOAP `charge` request.
- `soap-response.xml` — Successful SOAP response.
- `soap-fault.xml` — SOAP fault for a declined card.

---

# SOAP Integration

The external payment integration follows this flow:

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