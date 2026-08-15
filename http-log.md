# HTTP Request and Response Log

## Overview

This document records five HTTP requests made using `curl.exe -i` against the public JSONPlaceholder API. The `-i` option was used to include the HTTP response headers along with the response body. Four requests were successful, while the fifth request deliberately requested a non-existent resource to demonstrate a `404 Not Found` response.

---

## Request 1 — Get User 1

### Command

```powershell
curl.exe -i https://jsonplaceholder.typicode.com/users/1
```

### Response

```text

PS C:\Users\hp\campuseats> curl.exe -i https://jsonplaceholder.typicode.com/users/1
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 13:49:53 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-+2Y3G3w049iSZtw5t1mzSnunngE"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=zqdhBXmGtEHr1sIWhcRKEDIM3noxSmhieHvG1V5Jeto%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786791173"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=zqdhBXmGtEHr1sIWhcRKEDIM3noxSmhieHvG1V5Jeto%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786791173"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786791223
Age: 10619
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b8aa466c02fe23-SIN
alt-svc: h3=":443"; ma=86400

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
}
```

### Annotation

**Status:** `200 OK` — The server successfully processed the request and returned the requested user resource.

**Content-Type:** `application/json; charset=utf-8` — The response body is JSON data encoded using UTF-8.

**Returned resource:** User with ID `1`, including details such as name, username, email, address, phone, website, and company.

---

## Request 2 — Get User 2

### Command

```powershell
curl.exe -i https://jsonplaceholder.typicode.com/users/2
```

### Response

```text

PS C:\Users\hp\campuseats> curl.exe -i https://jsonplaceholder.typicode.com/users/2
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 13:56:56 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-XTG63SYhaP/Uo6/vgmARnL3rpBk"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=COoDh6twQJqSzJFqeQQm8iS4UZht9JmNC%2B4VzPmkUdU%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786788373"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=COoDh6twQJqSzJFqeQQm8iS4UZht9JmNC%2B4VzPmkUdU%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786788373"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 813
x-ratelimit-reset: 1786788403
Age: 13842
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2b8b49c18cfff8e-SIN
alt-svc: h3=":443"; ma=86400

{
  "id": 2,
  "name": "Ervin Howell",
  "username": "Antonette",
  "email": "Shanna@melissa.tv",
  "address": {
    "street": "Victor Plains",
    "suite": "Suite 879",
    "city": "Wisokyburgh",
    "zipcode": "90566-7771",
    "geo": {
      "lat": "-43.9509",
      "lng": "-34.4618"
    }
  },
  "phone": "010-692-6593 x09125",
  "website": "anastasia.net",
  "company": {
    "name": "Deckow-Crist",
    "catchPhrase": "Proactive didactic contingency",
    "bs": "synergize scalable supply-chains"
  }
}
```

### Annotation

**Status:** `200 OK` — The server successfully processed the request and returned the requested user resource.

**Content-Type:** `application/json; charset=utf-8` — The response body contains JSON data encoded using UTF-8.

**Returned resource:** User with ID `2`, including details such as name, username, email, address, phone, website, and company.

---

## Request 3 — Get Post 1

### Command

```powershell
curl.exe -i https://jsonplaceholder.typicode.com/posts/1
```

### Response

```text
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 14:00:39 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 292
Connection: keep-alive

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```

### Annotation

**Status:** `200 OK` — The request was successful and the requested post was returned.

**Content-Type:** `application/json; charset=utf-8` — The response contains JSON data encoded using UTF-8.

**Returned resource:** Post with ID `1`, belonging to user ID `1`.

---

## Request 4 — Get Comment 1

### Command

```powershell
curl.exe -i https://jsonplaceholder.typicode.com/comments/1
```

### Response

```text
HTTP/1.1 200 OK
Date: Sat, 15 Aug 2026 14:02:23 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 268
Connection: keep-alive

{
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusamus"
}
```

### Annotation

**Status:** `200 OK` — The server successfully processed the request and returned the requested comment.

**Content-Type:** `application/json; charset=utf-8` — The response body is JSON data encoded using UTF-8.

**Returned resource:** Comment with ID `1`, associated with post ID `1`.

---

## Request 5 — Deliberate 404

### Command

```powershell
curl.exe -i https://jsonplaceholder.typicode.com/users/9999
```

### Response

```text
HTTP/1.1 404 Not Found
Date: Sat, 15 Aug 2026 14:03:53 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2
Connection: keep-alive

{}
```

### Annotation

**Status:** `404 Not Found` — The requested resource does not exist. This request was deliberately made with a non-existent user ID (`9999`) to demonstrate an HTTP error response.

**Content-Type:** `application/json; charset=utf-8` — Even though the request failed, the server returned the response body in JSON format using UTF-8 encoding.

---

## Summary

| Request | Endpoint      | Status          | Content-Type                      |
| ------- | ------------- | --------------- | --------------------------------- |
| 1       | `/users/1`    | `200 OK`        | `application/json; charset=utf-8` |
| 2       | `/users/2`    | `200 OK`        | `application/json; charset=utf-8` |
| 3       | `/posts/1`    | `200 OK`        | `application/json; charset=utf-8` |
| 4       | `/comments/1` | `200 OK`        | `application/json; charset=utf-8` |
| 5       | `/users/9999` | `404 Not Found` | `application/json; charset=utf-8` |

## Conclusion

The five requests demonstrate how HTTP requests can be sent directly from the command line using `curl.exe`. The successful requests returned `200 OK`, while the deliberately invalid request returned `404 Not Found`. The `Content-Type` header showed that the API responses were provided as JSON encoded using UTF-8.
