# CampusEats â€“ README Sections

## Student Details

**Name:** Aman Kumar  
**Roll Number:** 20251651017

**Course:** CS543 – Web Services
**Tutorial:** 09 – API Security
---

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

### Demo Video and Screenshots

- **Assignment 8 Demo Video:** [Watch Demo / Open Google Drive Folder](https://drive.google.com/drive/folders/1GRYleDmb1VKBoqZ4Id442HeF4Ktoca6v?usp=sharing)
- **Before Screenshot:** `rest-menu-service/screenshots/before.png`
- **After Screenshot:** `rest-menu-service/screenshots/after.png`

---

## TUTORIAL-09 API Security: Authentication and Authorization

We secured the CampusEats REST Menu Service using JWT authentication and role-based authorization.

### Security Features

- Passwords are hashed using `bcryptjs`.
- JWT tokens are generated using `jsonwebtoken` after successful login.
- Tokens expire after one hour.
- Authentication middleware verifies JWT tokens.
- Authorization middleware checks user roles.
- Customers can view menu items.
- Restaurant users can add menu items.

### Demo User Credentials

| Role | Email | Password |
|---|---|---|
| Customer | `asha@campus.edu` | `customer123` |
| Restaurant | `mealhub@campus.edu` | `resto123` |

*These are demonstration credentials for the local lab only.*

### API Routes

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/login` | Public | Verify credentials and return a JWT |
| GET | `/items` | Authenticated users | Return all menu items |
| GET | `/items/:id` | Authenticated users | Return one menu item |
| POST | `/items` | Restaurant/Admin | Add a menu item |

### HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Menu item created |
| 401 | Invalid login, missing token, or invalid token |
| 403 | Authenticated user does not have permission |
| 404 | Menu item not found |
| 422 | Invalid or missing input data |

### Authentication and Authorization Flow

1. The user sends an email and password to `POST /login`.
2. The server checks the password using `bcryptjs`.
3. On successful login, the server generates a signed JWT containing the user ID and role.
4. The client sends the token in the `Authorization: Bearer <token>` header.
5. Authentication middleware verifies the token.
6. Authorization middleware checks the user's role before allowing restricted operations.

### Testing Results

| Test Case | Expected Result | Observed Result |
|---|---|---|
| GET `/items` without token | 401 | PASS |
| GET `/items` with invalid token | 401 | PASS |
| Customer login | JWT generated | PASS |
| Customer GET `/items` | 200 | PASS |
| Customer POST `/items` | 403 | PASS |
| Restaurant login | JWT generated | PASS |
| Restaurant POST `/items` | 201 | PASS |
| Login with incorrect password | 401 | PASS |
| Customer GET `/items/1` | 200 | PASS |

### Run API Security Module

```powershell
cd rest-menu-service
npm install
node server.js
```

Open `http://localhost:3000/` in your browser.

**Security Note:** The fallback JWT secret is for local development only. A deployed application should use a strong secret stored in an environment variable and HTTPS.

