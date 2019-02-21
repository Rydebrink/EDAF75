#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, post, run, response, request
import sqlite3
import json
import hashlib

HOST = 'localhost'
PORT = 7007

conn = sqlite3.connect("movies.db")

def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()



def format_response(d):
    return json.dumps(d, indent=4) + "\n"


def get_film_by_key(imdb_key):
	c = conn.cursor()
	c.execute(
		"""
		SELECT imdb_key, title, year
		FROM   films
		WHERE  imdb_key = ?
		""",
		[imdb_key]
	)
	return c


def imdb_key_exists(key):
	response.content_type = 'application/json'
	c = get_film_by_key(key)
	return c.fetchone() is not None


def theater_exists(key):
	response.content_type = 'application/json'
	c = conn.cursor()
	c.execute(
		"""
		SELECT t_name
		FROM   theatres
		WHERE  t_name = ?
		""",
		[key]
	)
	return c.fetchone() is not None

def performance_exists(p_id):
	response.content_type = 'application/json'
	c = conn.cursor()
	c.execute(
		"""
		SELECT p_id
		FROM   performances
		WHERE  p_id = ?
		""",
		[p_id]
	)
	result = c.fetchone()
	return result is not None

def user_exists(user_name):
	response.content_type = 'application/json'
	c = conn.cursor()
	c.execute(
		"""
		SELECT user_name
		FROM   customers
		WHERE  user_name = ?
		""",
		[user_name]
	)
	result = c.fetchone()
	return result is not None

def check_password(user, pwd):
	c = conn.cursor()
	c.execute(
		"""
		SELECT password
		FROM   customers
		WHERE  user_name= ?
		""",
		[user]
	)
	result = c.fetchone()
	return result is not None and result[0] == hash(pwd)

def tickets_left(p_id):
	c = conn.cursor()
	c.execute(
		"""
		SELECT (capacity - count(t_id))
		FROM   performances
		JOIN   theatres
		USING  (t_name)
		LEFT JOIN tickets
		USING  (p_id)
		WHERE  p_id = ?
		""",
		[p_id]
	)
	return c.fetchone()[0]


@get('/ping')
def get_ping():
	return "pong"


@post('/reset')
def post_reset():
	response.content_type = 'application/json'
	c = conn.cursor()
	c.executescript(
		"""
		DELETE FROM theatres;
		DELETE FROM films;
		DELETE FROM customers;
		DELETE FROM performances;
		DELETE FROM tickets;
		"""
	)
	c.execute(
		"""
		INSERT
		INTO   customers(user_name, full_name, password)
		VALUES
				('alice', 'Alice', ?),
				('bob', 'Bob', ?);
		""", [hash('dobido'), hash('whatsinaname')]
	)
	c.execute(
		"""
		INSERT
		INTO   films(title, year, imdb_key, runtime)
		VALUES
				('The Shape of Water', 2017, 'tt5580390', 123),
				('Moonlight', 2016, 'tt4975722', 111),
				('Spotlight', 2015, 'tt1895587', 129),
				('Birdman', 2014, 'tt2562232', 119);
		"""
	)
	c.execute(
		"""
		INSERT
		INTO   theatres(t_name, capacity)
		VALUES
				('Kino', 10),
				('Södran', 16),
				('Skandia', 100);
		"""
	)
	conn.commit()
	return "OK"


@get('/movies')
def get_films():
	response.content_type = 'application/json'
	query =	"""
		SELECT imdb_key, title, year
		FROM   films
		WHERE  1 = 1
		"""
	params = []
	if request.query.title:
		query += "AND title = ?"
		params.append(request.query.title)
	if request.query.year:
		query += "AND year = ?"
		params.append(request.query.year)
	c = conn.cursor()
	c.execute(
		query,
		params
	)
	s = [{"imdbKey": imdb_key, "title": title, "year": year}
		for (imdb_key, title, year) in c]
	return format_response({"data": s})


@get('/movies/<imdb_key>')
def get_film(imdb_key):
	response.content_type = 'application/json'
	c = get_film_by_key(imdb_key)
	s = [{"imdbKey": imdb_key, "title": title, "year": year}
		for (imdb_key, title, year) in c]
	# Set status code
	if len(s) < 1:
		response.status = 404
	return format_response({"data": s})


@post('/performances')
def post_performance():
	response.content_type = 'application/json'
	query =	"""
		INSERT
		INTO performances(imdb_key, t_name, date, time)
		VALUES (?, ?, ?, ?);
		"""
	params = []
	if request.query.imdb and request.query.theater and request.query.date and request.query.time:
		if imdb_key_exists(request.query.imdb) and theater_exists(request.query.theater):
			params.append(request.query.imdb)
			params.append(request.query.theater)
			params.append(request.query.date)
			params.append(request.query.time)
		else:
			response.status = 400
			return "No such movie or theater"
	else:
		response.status = 400
		return "Missing parameter"

	c = conn.cursor()
	c.execute(
		query,
		params
	)
	conn.commit()
	c.execute(
        """
        SELECT   p_id
        FROM     performances
        WHERE    rowid = last_insert_rowid()
        """
    )
	p_id = c.fetchone()[0]
	response.status = 200
	return "/performances/%s" % (p_id)


@get('/performances')
def get_performances():
	response.content_type = 'application/json'
	c = conn.cursor()
	c.execute(
		"""
		SELECT p_id, date, time, title, year, t_name, (capacity - count(t_id)) AS remaining_seats
		FROM   performances
		JOIN   films
		USING  (imdb_key)
		JOIN   theatres
		USING  (t_name)
		LEFT JOIN tickets
		USING  (p_id)
		GROUP BY p_id
		"""
	)
	s = [{"performanceId": p_id, "date": date, "startTime": time, "title" : title, "year" : year, "theater" : t_name, "remaining" : remaining_seats}
		for (p_id, date, time, title, year, t_name, remaining_seats) in c]
	return format_response({"data": s})


@post('/tickets')
def post_tickets():
	params = []
	if not (request.query.user and request.query.performance and request.query.pwd):
		response.status = 400
		return "Missing parameter"
	elif not (performance_exists(request.query.performance) and user_exists(request.query.user)):
		response.status = 400
		return "No such performance or user"
	elif not check_password(request.query.user, request.query.pwd):
		response.status = 401
		return "Wrong password"
	elif not tickets_left(request.query.performance):
		response.status = 403
		return "No tickets left"
	else:
		params.append(request.query.performance)
		params.append(request.query.user)
	c = conn.cursor()
	response.content_type = 'application/json'
	query =	"""
		INSERT
		INTO tickets(p_id, user_name)
		VALUES (?, ?);
		"""
	c.execute(
		query,
		params
	)
	conn.commit()
	c.execute(
        """
        SELECT   t_id
        FROM     tickets
        WHERE    rowid = last_insert_rowid()
        """
    )
	t_id = c.fetchone()[0]
	response.status = 200
	return "/tickets/%s" % (t_id)


run(host=HOST, port=PORT, debug=True)
