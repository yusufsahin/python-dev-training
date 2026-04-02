import os

import psycopg

from db.backend_kind import DbBackend

_POSTGRES_DSN = os.environ.get(
    "POSTGRES_DSN",
    "dbname=db_app01 user=postgres password=Aloha@2026 host=localhost port=5432",
)


def _postgres_connection_factory():
    def connect():
        return psycopg.connect(_POSTGRES_DSN)

    return connect


def _mysql_connection_factory():
    import pymysql

    host = os.environ.get("MYSQL_HOST", "127.0.0.1")
    port = int(os.environ.get("MYSQL_PORT", "3306"))
    user = os.environ.get("MYSQL_USER", "root")
    password = os.environ.get("MYSQL_PASSWORD", "")
    database = os.environ.get("MYSQL_DATABASE", "db_app01")

    def connect():
        return pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            autocommit=False,
        )

    return connect


def get_connection_for(backend: DbBackend):
    """Belirtilen motor için ConnectionFactory (çağrıldığında bağlantı döner)."""
    if backend == DbBackend.MYSQL:
        return _mysql_connection_factory()
    return _postgres_connection_factory()


def get_connection():
    """Ortam değişkenindeki DB_BACKEND için varsayılan ConnectionFactory."""
    from db.config import load_db_context

    return load_db_context().connect
