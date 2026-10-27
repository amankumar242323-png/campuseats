CREATE DATABASE IF NOT EXISTS campuseats_graphql;
USE campuseats_graphql;

CREATE TABLE IF NOT EXISTS dishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO dishes (name, price, available)
SELECT 'Paneer Roll', 90.00, TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM dishes WHERE name = 'Paneer Roll'
);

INSERT INTO dishes (name, price, available)
SELECT 'Veg Burger', 120.00, TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM dishes WHERE name = 'Veg Burger'
);

INSERT INTO dishes (name, price, available)
SELECT 'Masala Dosa', 80.00, TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM dishes WHERE name = 'Masala Dosa'
);

INSERT INTO dishes (name, price, available)
SELECT 'Cold Coffee', 60.00, TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM dishes WHERE name = 'Cold Coffee'
);
