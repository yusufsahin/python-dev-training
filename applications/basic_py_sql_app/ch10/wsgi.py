"""WSGI entry (Gunicorn: gunicorn wsgi:application)."""

from tasks import create_app

application = create_app()
