const express = require("express");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

let items = [
  { id: 1, name: "Paneer Roll", price: 90, available: true },
  { id: 2, name: "Veg Burger", price: 120, available: true },
  { id: 3, name: "Masala Dosa", price: 80, available: true },
  { id: 4, name: "Cold Coffee", price: 60, available: true }
];
let nextId = 5;

app.get("/items", (req, res) => res.status(200).json(items));

app.get("/items/:id", (req, res) => {
  const id = Number(req.params.id);
  const item = items.find((entry) => entry.id === id);
  if (!item) return res.status(404).json({ error: "Item not found" });
  return res.status(200).json(item);
});

app.post("/items", (req, res) => {
  const { name, price, available = true } = req.body || {};
  if (typeof name !== "string" || !name.trim()) {
    return res.status(422).json({ error: "name is required" });
  }
  if (price === undefined || price === null || price === "" ||
      !Number.isFinite(Number(price)) || Number(price) <= 0) {
    return res.status(422).json({ error: "price must be a positive number" });
  }
  if (typeof available !== "boolean") {
    return res.status(422).json({ error: "available must be true or false" });
  }
  const newItem = { id: nextId++, name: name.trim(), price: Number(price), available };
  items.push(newItem);
  return res.status(201).json(newItem);
});

app.use(express.static(path.join(__dirname, "public")));

app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && "body" in err) {
    return res.status(400).json({ error: "Invalid JSON body" });
  }
  return next(err);
});

app.listen(PORT, () => {
  console.log(`CampusEats REST Menu Service: http://localhost:${PORT}`);
  console.log(`Items API: http://localhost:${PORT}/items`);
});
