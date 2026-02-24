"""Veri katmanı: bağlantı, tablolar ve CRUD modülleri."""
from .db import get_connection, get_db_path, create_tables
from . import tasks as tasks_crud
from . import categories as categories_crud

__all__ = [
    "get_connection",
    "get_db_path",
    "create_tables",
    "tasks_crud",
    "categories_crud",
]
