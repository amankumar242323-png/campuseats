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
