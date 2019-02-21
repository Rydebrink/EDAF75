#!/bin/bash
#Tested:
curl -X GET http://localhost:7007/ping
#curl -X POST http://localhost:7007/reset
curl -X GET http://localhost:7007/movies
curl -X GET http://localhost:7007/movies\?title=Spotlight\&year=2015
curl -X GET http://localhost:7007/movies/tt5580390
#curl -X POST http://localhost:7007/performances\?imdb=tt5580390\&theater=Kino\&date=2019-02-22\&time=19:00
#curl -X POST http://localhost:7007/performances\?imdb=tt4975722\&theater=Skandia\&date=2019-02-22\&time=19:00
#curl -X POST http://localhost:7007/performances\?imdb=tt2562232\&theater=Södran\&date=2019-02-22\&time=19:00
curl -X GET http://localhost:7007/performances

#Untested:

curl -X POST http://localhost:7007/tickets\?user=alice\&performance=d76ec5f16fc4f588410a732386747d3f\&pwd=dobido
curl -X GET http://localhost:7007/customers/alice/tickets
