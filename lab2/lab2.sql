PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theatres;
DROP TABLE IF EXISTS films;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=ON;

CREATE TABLE theatres (
  t_name       TEXT,
  capacity		INT,
  PRIMARY KEY  (t_name)
);

CREATE TABLE films (
  imdb_key     TEXT,
  title        TEXT,
  year         INT,
  runtime      INT,
  PRIMARY KEY  (imdb_key)
);

CREATE TABLE customers (
  user_name    TEXT,
  full_name    TEXT,
  password     TEXT DEFAULT (lower(hex(randomblob(16)))),
  PRIMARY KEY  (user_name)
);

CREATE TABLE performances (
  p_id         INT DEFAULT (lower(hex(randomblob(16)))),
  date         DATE,
  time         TIME,
  imdb_key     TEXT,
  t_name       TEXT,
  PRIMARY KEY  (p_id),
  FOREIGN KEY  (imdb_key) REFERENCES films(imdb_key),
  FOREIGN KEY  (t_name)   REFERENCES theatres(t_name)
);

CREATE TABLE tickets (
  t_id         INT DEFAULT (lower(hex(randomblob(16)))),
  p_id         INT,
  user_name    TEXT,
  PRIMARY KEY  (t_id),
  FOREIGN KEY  (p_id)      REFERENCES performances(p_id),
  FOREIGN KEY  (user_name) REFERENCES customers(user_name)
);

INSERT
INTO   theatres(t_name, capacity)
VALUES ('Filmstaden', 120),
       ('Kino', 60),
       ('Bergakungen', 310),
       ('Grottan', 12);

INSERT
INTO   films(imdb_key, title, year, runtime)
VALUES ('tt0076759', 'Star Wars', 1977, 121),
       ('tt0082971', 'Raiders of the Lost Ark', 1981, 115),
       ('tt1034314', 'Iron Sky', 2012, 93),
       ('tt3521126', 'The Disaster Artist', 2017, 104);

INSERT
INTO   customers(user_name, full_name)
VALUES ('dat15asy', 'Axel Syrén'),
        ('dat14tsm', 'Tommy Smask'),
        ('dat15vcl', 'Viktor Claesson');

INSERT
INTO   performances(p_id, date, time, imdb_key, t_name)
VALUES (1, '2019-02-15', '17:30', 'tt0076759', 'Filmstaden'),
       (2, '2019-02-15', '19:20', 'tt1034314', 'Kino'),
       (3, '2019-02-15', '20:00', 'tt0082971', 'Filmstaden'),
       (4, '2019-03-10', '12:00', 'tt3521126', 'Grottan');

INSERT
INTO   performances(date, time, imdb_key, t_name)
VALUES ('2019-02-15', '15:00', 'tt0076759', 'Filmstaden'),
       ('2019-02-15', '22:30', 'tt0082971', 'Filmstaden'),
       ('2019-02-15', '21:55', 'tt1034314', 'Kino');

INSERT
INTO   tickets(p_id, user_name)
VALUES (1, 'dat15asy'),
       (2, 'dat15asy'),
       (3, 'dat15vcl'),
       (3, 'dat15vcl'),
       (3, 'dat15vcl'),
       (3, 'dat15vcl');
