PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS order_contents;
DROP TABLE IF EXISTS raw_material_transactions;

PRAGMA foreign_keys=ON;

CREATE TABLE recipes (
  name         TEXT,
  active       INT DEFAULT 1,
  PRIMARY KEY  (name)
);

CREATE TABLE ingredients (
  name         TEXT,
  amount       INT,
  recipe_name  TEXT,
  PRIMARY KEY  (name),
  FOREIGN KEY  (recipe_name) REFERENCES recipes(name)
);

CREATE TABLE customers (
  customer_id  INT,
  name         TEXT,
  address      TEXT,
  PRIMARY KEY  (customer_id)
);

CREATE TABLE orders (
  order_id        INT DEFAULT (lower(hex(randomblob(16)))),
  customer_id     INT,
  to_be_delivered DATE,
  PRIMARY KEY     (order_id),
  FOREIGN KEY     (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE pallets (
  pallet_id       INT      DEFAULT (lower(hex(randomblob(16)))),
  status          TEXT     DEFAULT 'ready',
  production_date DATE     DEFAULT CURRENT_DATE,
  delivery_time   DATETIME DEFAULT NULL,
  is_blocked      INT      DEFAULT 0,
  order_id        INT      DEFAULT NULL,
  recipe_name     TEXT,
  PRIMARY KEY     (pallet_id),
  FOREIGN KEY     (order_id) REFERENCES orders(order_id),
  FOREIGN KEY     (recipe_name) REFERENCES recipes(name)
);

CREATE TABLE order_contents (
  order_id    INT,
  recipe_name TEXT,
  nbr         INT,
  PRIMARY KEY (order_id, recipe_name),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (recipe_name) REFERENCES recipes(name)
);

CREATE TABLE raw_material_transactions (
  name        TEXT,
  amount      INT,
  time        DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (name, time)
);
