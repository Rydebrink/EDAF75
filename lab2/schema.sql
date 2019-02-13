DROP TABLE IF EXISTS theatres;
CREATE TABLE theatres (
  t_name       TEXT,
  capacity		INT,
  PRIMARY KEY  (t_name)
);

DROP TABLE IF EXISTS films;
CREATE TABLE films (
  imdb_key     TEXT,
  title        TEXT,
  year         INT,
  runtime      INT,
  PRIMARY KEY  (imdb_key)
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
  user_name    TEXT,
  full_name    TEXT,
  password     TEXT DEFAULT (lower(hex(randomblob(16)))),
  PRIMARY KEY  (user_name)
);

DROP TABLE IF EXISTS performances;
CREATE TABLE performances (
  p_id         INT DEFAULT (lower(hex(randomblob(16)))),
  time         TEXT,
  imdb_key     TEXT,
  t_name       TEXT,
  PRIMARY KEY  (p_id),
  FOREIGN KEY  (imdb_key) REFERENCES films(imdb_key),
  FOREIGN KEY  (t_name)   REFERENCES theatres(t_name)
);

DROP TABLE IF EXISTS tickets;
CREATE TABLE tickets (
  t_id         INT DEFAULT (lower(hex(randomblob(16)))),
  p_id         INT,
  user_name    TEXT,
  PRIMARY KEY  (t_id),
  FOREIGN KEY  (p_id)      REFERENCES performances(p_id),
  FOREIGN KEY  (user_name) REFERENCES customers(user_name)
);
