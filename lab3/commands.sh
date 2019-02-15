#!/bin/bash
#Tested:
curl -X GET http://localhost:7007/films
curl -X GET http://localhost:7007/ping
curl -X POST http://localhost:7007/reset
curl -X GET http://localhost:7007/films
curl -X GET http://localhost:7007/films\?title=Spotlight\&year=2015

#Untested:
#curl -X GET http://localhost:7007/films/<imdb-key>
#curl -X GET http://localhost:7007/films/tt5580390
#curl -X POST http://localhost:7007/performances\?imdb=<imdb>\&theatre=<theatre>\&date=<date>\&time=<time>
#curl -X POST http://localhost:7007/performances\?imdb=tt5580390\&theatre=Kino\&date=2019-02-22\&time=19:00
#curl -X GET http://localhost:7007/performances
#curl -X POST http://localhost:7007/tickets\?user=<user-id>\&performance=<performance-id>\&pwd=<pwd>
#curl -X POST http://localhost:7007/tickets\?user=alice\&performance=fd8d3790e16c110fc8ac50d84f408a3f\&pwd=dobido
#curl -X GET http://localhost:7007/customers/<customer-id>/tickets
#curl -X GET http://localhost:7007/customers/alice/tickets
