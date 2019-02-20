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


def imdb_key_exists(key):
	response.content_type = 'application/json'
	c = conn.cursor()
	c.execute(
		"""
		SELECT imdb_key, title, year
		FROM   films
		WHERE  imdb_key = ?
		""",
		[key]
	)
	if c.fetchone() is not None:
		return True
	else:
		return False

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
	if c.fetchone() is not None:
		return True
	else:
		return False

@get('/ping')
def get_ping():
	response.status = 200
#	s = [{'answer' : "pong"}]
#	return format_response({"data": s})
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
	conn.commit();
	response.status = 200
#	s = [{'answer' : "ok"}]
#	return format_response({"data": s})
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
	c = conn.cursor()
	c.execute(
		"""
		SELECT imdb_key, title, year
		FROM   films
		WHERE  imdb_key = ?
		""",
		[imdb_key]
	)
	s = [{"imdbKey": imdb_key, "title": title, "year": year}
		for (imdb_key, title, year) in c]
#	if c.rowcount > 0:
#		response.status = 200
#	else:
#		response.status = 404
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
			return format_response({"error": "No such movie or theater"})
	else:
		response.status = 400
		return format_response({"error": "Missing parameter"})

	c = conn.cursor()
	c.execute(
		query,
		params
	)
	c = conn.cursor()
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


run(host=HOST, port=PORT, debug=True)
