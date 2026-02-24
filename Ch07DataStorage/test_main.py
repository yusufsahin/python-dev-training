"""Birim testleri: main modülündeki veritabanı fonksiyonları (geçici DB = :memory:)."""
from __future__ import annotations

import sqlite3

import pytest

import main


@pytest.fixture
def use_memory_db(monkeypatch: pytest.MonkeyPatch) -> None:
    """Veritabanı kullanan testlerde :memory: kullanılır."""
    monkeypatch.setattr(main, "get_db_path", lambda: ":memory:")


def test_get_db_path_default(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ortam değişkeni yoksa varsayılan yol döner."""
    monkeypatch.delenv("DB_PATH", raising=False)
    assert main.get_db_path() == main.DEFAULT_DB_PATH


def test_get_db_path_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """DB_PATH ortam değişkeni varsa o kullanılır."""
    monkeypatch.setenv("DB_PATH", "/tmp/test.sqlite3")
    assert main.get_db_path() == "/tmp/test.sqlite3"


def test_get_connection_context_manager(use_memory_db: None) -> None:
    """get_connection context manager bağlantıyı açar, commit/close yapar."""
    with main.get_connection() as conn:
        assert conn is not None
        cur = conn.cursor()
        cur.execute("SELECT 1")
        assert cur.fetchone() == (1,)
    with pytest.raises(sqlite3.ProgrammingError):
        conn.execute("SELECT 1")


def test_create_table(use_memory_db: None) -> None:
    """create_table employees tablosunu oluşturur."""
    with main.get_connection() as conn:
        main.create_table(conn)
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='employees'"
            )
            assert cur.fetchone() is not None
        finally:
            cur.close()


def test_insert_employee(use_memory_db: None) -> None:
    """insert_employee tek kayıt ekler."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.insert_employee(conn, "Test", "User", 45000.0)
        rows = main.fetch_employees(conn)
    assert len(rows) == 1
    assert rows[0][1] == "Test" and rows[0][2] == "User" and rows[0][3] == 45000.0


def test_fetch_employees(use_memory_db: None) -> None:
    """fetch_employees tüm satırları list[tuple] olarak döndürür."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.insert_employee(conn, "A", "B", 1000.0)
        main.insert_employee(conn, "C", "D", 2000.0)
        rows = main.fetch_employees(conn)
    assert len(rows) == 2
    assert rows[0][1] == "A" and rows[0][2] == "B" and rows[0][3] == 1000.0
    assert rows[1][1] == "C" and rows[1][2] == "D" and rows[1][3] == 2000.0


def test_fetch_employee_by_id(use_memory_db: None) -> None:
    """fetch_employee_by_id id ile tek kayıt döner; yoksa None."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.insert_employee(conn, "A", "B", 1000.0)
        rows = main.fetch_employees(conn)
        emp_id = rows[0][0]
        row = main.fetch_employee_by_id(conn, emp_id)
    assert row is not None
    assert row[0] == emp_id and row[1] == "A" and row[2] == "B" and row[3] == 1000.0
    with main.get_connection() as conn:
        main.create_table(conn)
        assert main.fetch_employee_by_id(conn, 99999) is None


def test_update_employee(use_memory_db: None) -> None:
    """update_employee kayıt günceller; olmayan id için False döner."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.insert_employee(conn, "Old", "Name", 30000.0)
        rows = main.fetch_employees(conn)
        emp_id = rows[0][0]
        ok = main.update_employee(conn, emp_id, "New", "Name", 35000.0)
    assert ok is True
    with main.get_connection() as conn:
        main.create_table(conn)  # same :memory: is new each time, so recreate
        main.insert_employee(conn, "Old", "Name", 30000.0)
        rows = main.fetch_employees(conn)
        emp_id = rows[0][0]
        main.update_employee(conn, emp_id, "New", "Name", 35000.0)
        rows = main.fetch_employees(conn)
    assert rows[0][1] == "New" and rows[0][2] == "Name" and rows[0][3] == 35000.0
    with main.get_connection() as conn:
        main.create_table(conn)
        assert main.update_employee(conn, 99999, "X", "Y", 0.0) is False


def test_delete_employee(use_memory_db: None) -> None:
    """delete_employee kayıt siler; olmayan id için False döner."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.insert_employee(conn, "To", "Delete", 1000.0)
        rows = main.fetch_employees(conn)
        emp_id = rows[0][0]
        ok = main.delete_employee(conn, emp_id)
    assert ok is True
    with main.get_connection() as conn:
        main.create_table(conn)
        rows = main.fetch_employees(conn)
    assert len(rows) == 0
    with main.get_connection() as conn:
        main.create_table(conn)
        assert main.delete_employee(conn, 99999) is False


def test_get_sqlite_version(use_memory_db: None) -> None:
    """get_sqlite_version sürüm string'i döndürür."""
    with main.get_connection() as conn:
        version = main.get_sqlite_version(conn)
    assert isinstance(version, str)
    assert len(version) >= 1
    assert version != "unknown"


def test_ensure_seed_data_adds_when_empty(use_memory_db: None) -> None:
    """ensure_seed_data tablo boşsa 2 kayıt ekler."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.ensure_seed_data(conn)
        rows = main.fetch_employees(conn)
    assert len(rows) == 2
    assert rows[0][1] == "John" and rows[0][2] == "Doe" and rows[0][3] == 50000.0
    assert rows[1][1] == "Jane" and rows[1][2] == "Doe" and rows[1][3] == 60000.0


def test_ensure_seed_data_skips_when_not_empty(use_memory_db: None) -> None:
    """ensure_seed_data tabloda veri varsa ekleme yapmaz."""
    with main.get_connection() as conn:
        main.create_table(conn)
        main.insert_employee(conn, "Only", "One", 30000.0)
        main.ensure_seed_data(conn)
        rows = main.fetch_employees(conn)
    assert len(rows) == 1
    assert rows[0][1] == "Only" and rows[0][2] == "One"

