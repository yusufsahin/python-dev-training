"""WSGI entry (Gunicorn: gunicorn wsgi:application)."""

from school import create_app

application = create_app()
