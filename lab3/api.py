from bottle import get, run
import sqlite3
import json

conn = sqlite3.connect("movies.db")

@get('/films')
def get_films():
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


run(host='localhost', port=4568)
