#!/usr/bin/env python
"# -*- coding: utf-8 -*-"

import json
import re
import requests


HOST="localhost"
PORT=7007


def url(resource):
    return "http://%s:%s%s" % (HOST, PORT, resource)


def response_to_dicts(r):
    return (dict(d) for d in r.json()['data'])


def abort(msg):
    print("Error: %s" % (msg))
    exit(1)


def check_ping():
    resource = url('/ping')
    r = requests.get(resource)
    if r.text.strip() == 'pong':
        print("ping OK")
    else:
        abort('curl -X GET %s does not return pong' % (resource))


def check_reset():
    resource = url('/reset')
    r = requests.post(resource)
    if r.text.strip() == 'OK':
        print("reset OK")
    else:
        abort('curl -X POST %s does not return OK' % (resource))
    

def check_all_movies():
    try:
        r = requests.get(url('/movies'))
        found = response_to_dicts(r)
        print("======== Found movies ========")
        for d in found:
            title = d['title']
            year = d['year']
            print("%s (%s)" % (title, year))
        print("==============================")
    except:
        abort("curl -X GET %s does not work" % (url('/movies')))


def check_movie_title(title, year):
    resource = url('/movies?title=%s&year=%s' % (title, year))
    try:
        r = requests.get(resource)
        found = list(response_to_dicts(r))
        if len(found) != 1:
            abort("curl -X GET %s returns %s movies (should have been 1)" % (resource, len(found)))
        for d in found:
            assert d['title'] == title
            assert d['year'] == year
        print("Could get %s (%s) using title and year" % (title, year))
    except:
        abort("curl -X GET %s does not work" % (resource))


def check_movie_imdb(imdb_key):
    resource = url('/movies/%s' % (imdb_key))
    try:
        r = requests.get(resource)
        found = list(response_to_dicts(r))
        if len(found) != 1:
            abort("%s returns %s movies (should have been 1)" % (resource, len(found)))
        for d in found:
            title = d['title']
            year = d['year']
        print("Could get %s (%s) using imdb-key" % (title, year))
    except:
        abort("curl -X GET %s does not work" % (resource))


def add_performances(imdb, theaters, dates):
    print("======== Adding performances ========")
    for theater in theaters:
        for date in dates:
            resource = url('/performances?imdb=%s&theater=%s&date=%s&time=19:30' % (imdb, theater, date))
            try:
                r = requests.post(resource)
                m = re.search('/performances/(.+)', r.text.strip())
                if m:
                    print("%s at %s on %s: %s" % (imdb, theater, date, m.group(1)))
            except:
                abort("curl -X POST %s does not work" % (url))
    print("-------------------------------------")
    print("See tickets at:")
    print("curl -GET %s" % (url('/performances')))
    print("=====================================")


def buy_tickets(user_id):
    print("======== Buying tickets ========")
    try:
        for _ in range(2):
            resource = url('/performances')
            r = requests.get(resource)
            performance = next(p for p in response_to_dicts(r) if p['theater'] == 'Kino' and p['remaining'] > 0)
            perf_id = performance['performanceId']
            seats_left = performance['remaining']
            print("================================")
            print("Buying tickets to %s on %s" % (performance['title'], performance['date']))
            buy_url = url('/tickets?user=%s&performance=%s&pwd=dobido' % (user_id, perf_id))
            print("--------------------------------")
            print(buy_url)
            print("--------------------------------")
            for _ in range(seats_left):
                r = requests.post(buy_url)
                print(r.text)
                m = re.search('/tickets/(.+)', r.text.strip())
                if not m:
                    abort('Got no ticket when trying to buy available seat')
            # now fail once:
            r = requests.post(buy_url)
            if not r.text.strip() == "No tickets left":
                abort("Could by too many tickets")
        print("================================")
    except:
        abort('Got error when trying to buy tickets')


def see_tickets(user_id):
    try:
        resource = url('/customers/%s/tickets' % (user_id))
        print("curl -X GET %s" % (resource))
        r = requests.get(resource)
        print(r.text)
    except:
        abort("Could not see the tickets bought by %s" % (user_id))


def main():
    check_ping()
    check_reset()
    check_all_movies()
    check_movie_title("Spotlight", 2015)
    check_movie_imdb("tt5580390")
    add_performances(
        'tt5580390',
        ['Kino', 'Skandia'],
        ['2019-02-22', '2019-02-23']
    )
    add_performances(
        'tt2562232',
        ['Kino', 'Skandia'],
        ['2019-02-24', '2019-02-25']
    )
    buy_tickets('alice')
    see_tickets('alice')
    print("=========================")
    print("I found no obvious errors")
    print("=========================")


if __name__ == '__main__':
    main()
