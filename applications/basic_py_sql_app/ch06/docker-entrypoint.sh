#!/bin/sh
set -e
cd /app
python manage.py migrate --noinput
python manage.py ensure_initial_data
python manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 4
