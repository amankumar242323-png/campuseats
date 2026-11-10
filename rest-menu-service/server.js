
require("dotenv").config();
const express = require("express");
const path = require("path");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const SECRET = process.env.JWT_SECRET;
if (!SECRET) throw new Error("JWT_SECRET is missing from environment");

// Users: passwords are stored as bcrypt hashes
const users = [
  {
    id: 1,
    email: "asha@campus.edu",
    role: "customer",
    hash: bcrypt.hashSync("customer123", 10)
  },
  {
    id: 2,
    email: "mealhub@campus.edu",
    role: "restaurant",
    hash: bcrypt.hashSync("resto123", 10)
  }
];

// Existing menu items
let items = [
  { id: 1, name: "Paneer Roll", price: 90, available: true },
  { id: 2, name: "Veg Burger", price: 120, available: true },
  { id: 3, name: "Masala Dosa", price: 80, available: true },
  { id: 4, name: "Cold Coffee", price: 60, available: true }
];

let nextId = 5;

// LOGIN API
app.post("/login", (req, res) => {
  const { email, password } = req.body || {};

  const user = users.find((u) => u.email === email);

  if (!user || !bcrypt.compareSync(password || "", user.hash)) {
    return res.status(401).json({ error: "bad login" });
  }

  const token = jwt.sign(
    { sub: user.id, role: user.role },
    SECRET,
    { expiresIn: "1h" }
  );

  return res.json({ token });
});

// AUTHENTICATION MIDDLEWARE
function auth(req, res, next) {
  const token = (req.get("Authorization") || "").split(" ")[1];

  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    return res.status(401).json({
      error: "invalid or missing token"
    });
  }
}

// AUTHORIZATION MIDDLEWARE
function requireRole(...allowed) {
  return (req, res, next) => {
    if (allowed.includes(req.user.role)) {
      return next();
    }

    return res.status(403).json({ error: "forbidden" });
  };
}

// GET ALL ITEMS - authenticated users
app.get("/items", auth, (req, res) => {
  return res.status(200).json(items);
});

// GET SINGLE ITEM - authenticated users
app.get("/items/:id", auth, (req, res) => {
  const id = Number(req.params.id);
  const item = items.find((entry) => entry.id === id);

  if (!item) {
    return res.status(404).json({ error: "Item not found" });
  }

  return res.status(200).json(item);
});

// POST ITEM - restaurant/admin only
app.post("/items", auth, requireRole("restaurant", "admin"), (req, res) => {
  const { name, price, available = true } = req.body || {};

  if (typeof name !== "string" || !name.trim()) {
    return res.status(422).json({ error: "name is required" });
  }

  if (
    price === undefined ||
    price === null ||
    price === "" ||
    !Number.isFinite(Number(price)) ||
    Number(price) <= 0
  ) {
    return res.status(422).json({
      error: "price must be a positive number"
    });
  }

  if (typeof available !== "boolean") {
    return res.status(422).json({
      error: "available must be true or false"
    });
  }

  const newItem = {
    id: nextId++,
    name: name.trim(),
    price: Number(price),
    available
  };

  items.push(newItem);

  return res.status(201).json(newItem);
});

// Serve frontend
app.use(express.static(path.join(__dirname, "public")));

app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && "body" in err) {
    return res.status(400).json({ error: "Invalid JSON body" });
  }
  return next(err);
});

app.listen(PORT, () => {
  console.log(`Secured CampusEats API: http://localhost:${PORT}`);
});

