"""Veritabanı türü ve bağlantı — ortam değişkenleriyle seçilir.

Ortam değişkenleri:
  DB_BACKEND — ``postgresql`` (varsayılan) veya ``mysql`` / ``mariadb``

PostgreSQL:
  POSTGRES_DSN — psycopg bağlantı dizesi (ör. ``dbname=... user=...``).
  Yerel varsayılan: ``db_app01`` veritabanı.

MySQL / MariaDB:
  MYSQL_HOST (127.0.0.1), MYSQL_PORT (3306), MYSQL_USER, MYSQL_PASSWORD,
  MYSQL_DATABASE (db_app01). Veritabanını önce oluşturmanız gerekir.
"""

import os
from dataclasses import dataclass

from db.backend_kind import DbBackend
from ports import ConnectionFactory


@dataclass(frozen=True)
class DbContext:
    connect: ConnectionFactory
    backend: DbBackend


def _env_backend() -> DbBackend:
    raw = os.environ.get("DB_BACKEND", "postgresql").strip().lower()
    if raw in ("mysql", "mariadb"):
        return DbBackend.MYSQL
    return DbBackend.POSTGRESQL


def load_db_context() -> DbContext:
    """DB_BACKEND ve bağlantı ortam değişkenlerinden DbContext üretir."""
    backend = _env_backend()
    from db import connection as conn_mod

    return DbContext(connect=conn_mod.get_connection_for(backend), backend=backend)
