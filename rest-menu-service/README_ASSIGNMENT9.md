# CampusEats – Assignment 09: Securing the API

## Team Details

**Course:** CS543 – Web Services  
**Assignment:** 09 – Securing the API  
**Group ID:** 02

| Sr. No. | Student Name | Roll Number |
|---|---|---|
| 1 | Aman Kumar | 20251651017 |
| 2 | Shrikanta Nayak | To be added |
| 3 | Aditya Verma | To be added |
| 4 | Pratik Sinha | To be added |

## 1. Project Overview

In Assignment 09, we secured the existing CampusEats REST Menu Service developed in Assignment 08 using JWT authentication and role-based authorization.

The objective was to implement secure login, password hashing, token verification, and role-based access control without creating a new service.

## 2. Technologies Used

- Node.js
- Express.js
- JSON Web Token (jsonwebtoken)
- bcryptjs
- dotenv
- HTML and CSS

## 3. Demo Users

| Role | Email | Password |
|---|---|---|
| Customer | asha@campus.edu | customer123 |
| Restaurant | mealhub@campus.edu | resto123 |

Passwords are stored as bcrypt hashes and verified using `bcrypt.compareSync()`.

*These credentials are for local educational demonstration only.*

## 4. API Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/login` | Public | Authenticate user and generate JWT |
| GET | `/items` | Authenticated users | Retrieve all menu items |
| GET | `/items/:id` | Authenticated users | Retrieve a menu item by ID |
| POST | `/items` | Restaurant/Admin | Add a new menu item |

## 5. Security Implementation

### 5.1 Password Hashing

User passwords are stored as bcrypt hashes instead of plain text.

### 5.2 Login and JWT Generation

The `POST /login` endpoint verifies user credentials. After successful authentication, the server generates a signed JWT containing the user ID and role.

The token expires after one hour.

### 5.3 Authentication Middleware

The `auth` middleware reads the Bearer token from the Authorization header and verifies it using `jwt.verify()`.

Missing, invalid, or expired tokens result in HTTP 401 Unauthorized.

### 5.4 Role-Based Authorization

The `requireRole()` middleware checks the authenticated user's role.

Only restaurant or admin users can add menu items. An authenticated customer attempting this operation receives HTTP 403 Forbidden.

### 5.5 Environment Configuration

The JWT secret is loaded using `dotenv` from the `JWT_SECRET` environment variable.

- `.env` stores the local secret and is excluded from Git.
- `.env.example` contains a blank `JWT_SECRET` value.
- The secret is not hardcoded in the application source code.

## 6. Assignment Questions and Answers

### Q1. Which routes require only authentication, and which also require a role?

- `GET /items` – Requires authentication only.
- `GET /items/:id` – Requires authentication only.
- `POST /items` – Requires authentication and the restaurant or admin role.
- `POST /login` – Public route used to authenticate users and obtain a JWT.

### Q2. Show one 401 and one 403 from your demo. Why did the server return that code?

**401 Unauthorized:** A GET `/items` request without a valid JWT returned HTTP 401 because the request was not authenticated.

**403 Forbidden:** A POST `/items` request using a valid customer token returned HTTP 403 because the customer was authenticated but did not have permission to add menu items.

### Q3. What is inside your JWT payload? Why is it safe to trust the role claim on the server, and why must the secret stay out of your code?

The JWT payload contains:

- `sub`: User ID
- `role`: User role (customer or restaurant)
- `iat`: Issued-at timestamp
- `exp`: Expiration timestamp

The server verifies the JWT signature using `jwt.verify()` and the secret before trusting the payload. If the signed payload is modified, signature verification fails.

The JWT secret must remain outside the source code to prevent unauthorized users from accessing it and generating forged tokens. It is loaded from the environment variable `JWT_SECRET`.

## 7. Testing Results

The following test cases were executed successfully:

| Test Case | Expected HTTP Status | Result |
|---|---:|---|
| GET `/items` without token | 401 | PASS |
| Customer login | 200 | PASS |
| GET `/items` with customer token | 200 | PASS |
| Restaurant login | 200 | PASS |
| Restaurant POST `/items` | 201 | PASS |
| Customer POST `/items` | 403 | PASS |

## 8. How to Run the Project

### Step 1: Navigate to the service directory

```powershell
cd rest-menu-service
```

### Step 2: Install dependencies

```powershell
npm install
```

### Step 3: Configure environment variables

Create a `.env` file using `.env.example` as a template and provide a strong secret:

```env
JWT_SECRET=your_strong_secret_here
```

### Step 4: Start the server

```powershell
npm start
```

The API runs at:

`http://localhost:3000`

Open the URL in a browser to access the frontend.

## 9. Demo and Screenshots

The demonstration covers the five required security cases:

1. Request without token – HTTP 401.
2. Successful login – JWT generated.
3. Request with a valid token – HTTP 200.
4. Restaurant adds a menu item – HTTP 201.
5. Customer attempts to add a menu item – HTTP 403.

**Demo Video:** Add the Google Drive link here.

**Screenshots:** Add the Google Drive folder link containing the five test screenshots here.

## 10. Conclusion

Through this assignment, we secured the existing CampusEats REST Menu Service using JWT authentication and role-based authorization. We implemented bcrypt password hashing, token generation and verification, middleware-based access control, and environment-based secret configuration.

The implementation demonstrates how authentication identifies users and authorization controls what actions they are permitted to perform.