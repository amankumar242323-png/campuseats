-- ==========================================
-- Identity Service
-- Owner: Srikanta Nayak
-- ==========================================

CREATE TABLE roles (
    role_id INTEGER PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);


-- ==========================================
-- Catalogue Service
-- Owner: Pratik Sinha
-- ==========================================

CREATE TABLE restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(200)
);

CREATE TABLE menus (
    menu_id INTEGER PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    name VARCHAR(150) NOT NULL,
    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
);

CREATE TABLE food_items (
    item_id INTEGER PRIMARY KEY,
    menu_id INTEGER NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (menu_id)
        REFERENCES menus(menu_id)
);


-- ==========================================
-- Order Service
-- Owner: Aditya Verma
-- ==========================================

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    status VARCHAR(30) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- ==========================================
-- Payment Service
-- Owner: Aman Kumar
-- ==========================================

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL
);