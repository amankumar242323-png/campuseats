# CampusEats

**Course:** CS543  
**Group ID:** 02

## Group Members

1. **AMAN KUMAR** — 20251651017
2. **SRIKANTA NAYAK** — 20251651090
3. **ADITYA VERMA** — 20251651009
4. **PRATIK SINHA** — 20251651071

## Project Overview

CampusEats is a campus food-service system project for CS543.

This repository contains the practical work related to HTTP requests, browser network analysis, Git, service-oriented system design, service contracts, database schema design, and the CampusEats system brief.

## Files

* `README.md` — Project overview and group information.
* `http-log.md` — Five HTTP request/response experiments using `curl.exe`.
* `network-analysis.md` — Analysis of website requests using Chrome DevTools Network panel.
* `brief.md` — CampusEats system brief describing what, who, nouns, and verbs.
* `design.pdf` — CampusEats service, contract, operation, schema, and validation design.
* `services.drawio` — Editable service design diagram.
* `services.png` — Exported service design diagram.
* `schema.drawio` — Editable database ER diagram.
* `schema.png` — Exported database ER diagram.
* `schema.sql` — Database `CREATE TABLE` statements.
* `docs/` — Additional project documentation.

## Tasks Completed

### Assignment 1 — HTTP by Hand & Project Setup

1. HTTP requests using curl
2. Browser Network analysis
3. Git repository setup
4. CampusEats system brief

### Assignment 2 — Services, Contracts & Schema

1. Capability identification
2. Service design
3. Service contracts
4. `placeOrder` full specification
5. Database schema design
6. Service validation

## Services

CampusEats is divided into four services:

- **Identity Service** — Responsible for identity and user-related data.
- **Order Service** — Responsible for orders and order-related data.
- **Catalogue Service** — Responsible for restaurants, menus, and food items.
- **Payment Service** — Responsible for payment processing and payment status.

Each service has its own data ownership boundary and defined service contract.

## Database Design

The database schema follows the service ownership boundary:

| Service | Data Owned |
|---|---|
| Identity Service | Users, Roles |
| Catalogue Service | Restaurants, Menus, Food Items |
| Order Service | Orders, Order Items |
| Payment Service | Payments |

No table is shared between two services.

## Central Operation

The central operation of CampusEats is:

```text
placeOrder
