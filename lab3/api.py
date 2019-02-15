#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, run, response
import sqlite3
import json
import hashlib

conn = sqlite3.connect("movies.db")

def hash(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


@get('/films')
def get_films():
    response.content_type = 'application/json'
    c = conn.cursor()
    c.execute(
        """
        SELECT *
        FROM   films
        """
    )
    s = [{"imdb_key": imdb_key, "title": title, "year": year, "runtime": runtime}
         for (imdb_key, title, year, runtime) in c]
    return json.dumps({"data": s}, indent=4)


@get('/ping')
def get_ping():
	s = [{'answer' : "pong"}]
	response.status = 200
	return json.dumps({"data": s}, indent=4)


@get('/reset')
def get_reset():
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
	s = [{'answer' : "ok"}]
	response.status = 200
	return json.dumps({"data": s}, indent=4)


run(host='localhost', port=7007)
