#!/bin/bash
sqlite3 db.sqlite < schema.sql
sqlite3 db.sqlite < sample_data.sql
sqlite3 db.sqlite < sample.sql
