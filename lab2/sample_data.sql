DELETE FROM theatres;
DELETE FROM films;
DELETE FROM customers;
DELETE FROM performances;
DELETE FROM tickets;

INSERT
INTO   theatres(t_name, capacity)
VALUES ('Filmstaden', 120),
       ('Kino', 60);

INSERT
INTO   films(imdb_key, title, year, runtime)
VALUES ('tt0076759', 'Star Wars', 1977, 121),
       ('tt0082971', 'Raiders of the Lost Ark', 1981, 115),
       ('tt1034314', 'Iron Sky', 2012, 93);

INSERT
INTO   customers(user_name, full_name)
VALUES ('dat15asy', 'Axel Syrén');

INSERT
INTO   performances(p_id, time, imdb_key, t_name)
VALUES (1, '17:30', 'tt0076759', 'Filmstaden'),
       (2, '19:20', 'tt1034314', 'Kino'),
       (3, '20:00', 'tt0082971', 'Filmstaden');

INSERT
INTO   performances(time, imdb_key, t_name)
VALUES ('15:00', 'tt0076759', 'Filmstaden'),
       ('22:30', 'tt0082971', 'Filmstaden'),
       ('21:55', 'tt1034314', 'Kino');

INSERT
INTO   tickets(p_id, user_name)
VALUES (1, 'dat15asy'),
       (2, 'dat15asy');
