"""Veritabanı bağlantısı ve tablo oluşturma. Ch07DataStorage kalıbı kullanılır."""
from __future__ import annotations

import logging
import os
import sqlite3
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DEFAULT_DB_NAME = "tasks.db"


def get_db_path() -> str:
    """Veritabanı dosya yolunu döndürür; DB_PATH ortam değişkeni yoksa uygulama dizininde tasks.db."""
    path = os.environ.get("DB_PATH")
    if path:
        return path
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, DEFAULT_DB_NAME)


@contextmanager
def get_connection():
    """Context manager ile bağlantı; otomatik commit/rollback ve close."""
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_tables(conn: sqlite3.Connection) -> None:
    """categories ve tasks tablolarını oluşturur (yoksa)."""
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER,
                status TEXT NOT NULL,
                due_date TEXT,
                category_id INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
    finally:
        cur.close()
