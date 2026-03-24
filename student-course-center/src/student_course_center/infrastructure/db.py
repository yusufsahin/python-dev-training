from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Sequence

import pyodbc

_ENV_KEY = "STUDENT_COURSE_CENTER_CONNECTION_STRING"


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(Path.cwd() / ".env")
    except ImportError:
        pass


def get_connection_string() -> str:
    _load_dotenv()
    cs = os.environ.get(_ENV_KEY, "").strip()
    if not cs:
        raise RuntimeError(
            f"Set environment variable {_ENV_KEY} to a SQL Server ODBC connection string."
        )
    return cs


def get_connection() -> pyodbc.Connection:
    return pyodbc.connect(get_connection_string())


def fetch_all(sql: str, params: Sequence[Any] | None = None) -> tuple[list[str], list[pyodbc.Row]]:
    params = params or ()
    with get_connection() as conn:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql, params)
        columns = [c[0] for c in cur.description] if cur.description else []
        rows = cur.fetchall()
        return columns, rows


def rows_as_dicts(columns: list[str], rows: Sequence[pyodbc.Row]) -> list[dict[str, Any]]:
    return [dict(zip(columns, row, strict=True)) for row in rows]


def execute_non_query(sql: str, params: Sequence[Any] | None = None) -> None:
    params = params or ()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()


def execute_scalar(sql: str, params: Sequence[Any] | None = None) -> Any:
    params = params or ()
    with get_connection() as conn:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]


def insert_returning_scalar(sql: str, params: Sequence[Any] | None = None) -> Any:
    """Single-row INSERT ... OUTPUT INSERTED.<Col> ... VALUES (...). Returns first column."""
    params = params or ()
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        row = cur.fetchone()
        conn.commit()
        if row is None:
            raise RuntimeError("insert_returning_scalar: no OUTPUT row returned")
        return row[0]
