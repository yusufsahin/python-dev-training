#!/bin/sh
set -e
cd /app
flask db upgrade
flask ensure-initial-data
exec gunicorn wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 4
