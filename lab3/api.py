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


@get('/ping')
def get_ping():
	s = [{'answer' : "pong"}]
	response.status = 200
	return format_response({"data": s})


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
	s = [{'answer' : "ok"}]
	response.status = 200
	return format_response({"data": s})


@get('/films')
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



run(host=HOST, port=PORT, debug=True)
