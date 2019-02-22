.headers on
.mode tabs

DELETE FROM performances;
DELETE FROM tickets;

INSERT
INTO   performances(p_id, date, time, imdb_key, t_name)
VALUES ('1', '2019-02-22', '19:00', 'tt5580390', 'Kino'),
       ('2', '2019-02-23', '19:00', 'tt4975722', 'Skandia');

INSERT
INTO   tickets(p_id, user_name)
VALUES (1, 'alice'),
       (1, 'alice'),
       (2, 'alice'),
       (1, 'bob'),
       (2, 'bob');


SELECT   date, time, t_name, title, year, count()
FROM     tickets
JOIN     performances
USING    (p_id)
JOIN     films
USING    (imdb_key)
WHERE    user_name = 'alice'
GROUP BY p_id;
