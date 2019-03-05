DELETE FROM recipes;
DELETE FROM ingredients;
DELETE FROM customers;
DELETE FROM orders;
DELETE FROM pallets;
DELETE FROM order_contents;
DELETE FROM raw_material_transactions;

INSERT
INTO   recipes(name)
VALUES ('Tango');


INSERT
INTO   ingredients(name, amount, recipe_name)
VALUES ('Butter', 200, 'Tango'),
       ('Sugar', 250, 'Tango'),
       ('Flour', 300, 'Tango'),
       ('Sodium bicarbonate', 4, 'Tango'),
       ('Vanilla', 2, 'Tango');

INSERT
INTO   customers(customer_id, name, address)
VALUES (1, 'Finkakor AB', 'Helsingborg'),
       (2, 'Småkakor AB', 'Malmö'),
       (3, 'Kaffebröd AB', 'Landskrona'),
       (4, 'Bjudkakor AB', 'Ystad'),
       (5, 'Kalaskakor AB', 'Trelleborg'),
       (6, 'Partykakor AB', 'Kristianstad'),
       (7, 'Gästkakor AB', 'Hässleholm'),
       (8, 'Skånekakor AB', 'Perstorp');

INSERT
INTO   orders(order_id, customer_id, to_be_delivered)
VALUES (137, 1, date('now','+21 day'));

INSERT
INTO   pallets(recipe_name)
VALUES ('Tango'),
       ('Tango');

INSERT
INTO   order_contents(order_id, recipe_name, nbr)
VALUES (137, 'Tango', 1);

INSERT
INTO   raw_material_transactions(name, amount)
VALUES ('Butter', 1000),
       ('Sugar', 1000),
       ('Flour', 1000),
       ('Sodium bicarbonate', 100),
       ('Vanilla', 100);
