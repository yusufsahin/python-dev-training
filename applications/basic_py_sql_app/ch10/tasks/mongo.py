"""MongoEngine connection (Flask app factory)."""

from __future__ import annotations

from flask import Flask
from mongoengine import connect


def init_mongo(app: Flask) -> None:
    connect(host=app.config["MONGODB_URI"], alias="default")
