from __future__ import annotations

import logging
import os
import sqlite3
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = "myDB.sqlite3"


def get_db_path() -> str:
    """Veritabanı dosya yolunu döndürür; DB_PATH ortam değişkeni yoksa varsayılan kullanılır."""
    return os.environ.get("DB_PATH", DEFAULT_DB_PATH)


@contextmanager
def get_connection():
    """Context manager ile bağlantı; otomatik commit/rollback ve close."""
    conn = sqlite3.connect(get_db_path())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def create_table(conn: sqlite3.Connection) -> None:
    """employees tablosunu oluşturur (yoksa). Sütunlar: id, first_name, last_name, annual_salary."""
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                annual_salary REAL
            )
        """)
    finally:
        cur.close()


def insert_employee(
    conn: sqlite3.Connection,
    first_name: str,
    last_name: str,
    annual_salary: float,
) -> None:
    """first_name, last_name ve annual_salary ile tek bir çalışan ekler."""
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO employees (first_name, last_name, annual_salary) VALUES (?, ?, ?)",
            (first_name, last_name, annual_salary),
        )
    finally:
        cur.close()


def fetch_employees(conn: sqlite3.Connection) -> list[tuple[int, str, str, float]]:
    """Tüm çalışanları (id, first_name, last_name, annual_salary) tuple listesi olarak döndürür."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, first_name, last_name, annual_salary FROM employees")
        return cur.fetchall()
    finally:
        cur.close()


def fetch_employee_by_id(
    conn: sqlite3.Connection, emp_id: int
) -> tuple[int, str, str, float] | None:
    """Belirtilen id'deki çalışanı döndürür; yoksa None."""
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT id, first_name, last_name, annual_salary FROM employees WHERE id=?",
            (emp_id,),
        )
        row = cur.fetchone()
        return row if row is not None else None
    finally:
        cur.close()


def update_employee(
    conn: sqlite3.Connection,
    emp_id: int,
    first_name: str,
    last_name: str,
    annual_salary: float,
) -> bool:
    """Belirtilen id'deki çalışanı günceller. Kayıt yoksa False döner."""
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE employees SET first_name=?, last_name=?, annual_salary=? WHERE id=?",
            (first_name, last_name, annual_salary, emp_id),
        )
        return cur.rowcount > 0
    finally:
        cur.close()


def delete_employee(conn: sqlite3.Connection, emp_id: int) -> bool:
    """Belirtilen id'deki çalışanı siler. Kayıt yoksa False döner."""
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
        return cur.rowcount > 0
    finally:
        cur.close()


def get_sqlite_version(conn: sqlite3.Connection) -> str:
    """SQLite sürümünü döndürür."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT sqlite_version()")
        row = cur.fetchone()
        return row[0] if row else "unknown"
    finally:
        cur.close()


def ensure_seed_data(conn: sqlite3.Connection) -> None:
    """Tablo boşsa örnek veri ekler (first_name, last_name, annual_salary); doluysa ekleme yapmaz."""
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM employees")
        (count,) = cur.fetchone()
    finally:
        cur.close()
    if count == 0:
        insert_employee(conn, "John", "Doe", 50000.0)
        insert_employee(conn, "Jane", "Doe", 60000.0)


def main() -> None:
    """Menü döngüsü: View / Create / Edit / Delete employees, Exit."""
    try:
        with get_connection() as conn:
            create_table(conn)
            ensure_seed_data(conn)
    except sqlite3.Error as e:
        logger.error("Veritabanı hatası: %s", e)
        raise

    while True:
        print()
        print("--- Employees ---")
        print("1) View employees")
        print("2) View by id")
        print("3) Create employee")
        print("4) Edit employee")
        print("5) Delete employee")
        print("6) Exit")
        choice = input("Seçiminiz (1-6): ").strip()

        if choice == "1":
            try:
                with get_connection() as conn:
                    rows = fetch_employees(conn)
                if not rows:
                    print("Kayıt yok.")
                else:
                    for row in rows:
                        emp_id, first_name, last_name, annual_salary = row
                        print(f"  id={emp_id} {first_name} {last_name} annual_salary={annual_salary}")
            except sqlite3.Error as e:
                logger.error("Veritabanı hatası: %s", e)
                print(f"Hata: {e}")

        elif choice == "2":
            try:
                emp_id = int(input("Id: ").strip())
            except ValueError:
                print("Geçersiz id.")
                continue
            try:
                with get_connection() as conn:
                    row = fetch_employee_by_id(conn, emp_id)
                if row is None:
                    print("Kayıt bulunamadı.")
                else:
                    eid, first_name, last_name, annual_salary = row
                    print(f"  id={eid} {first_name} {last_name} annual_salary={annual_salary}")
            except sqlite3.Error as e:
                logger.error("Veritabanı hatası: %s", e)
                print(f"Hata: {e}")

        elif choice == "3":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            try:
                annual_salary = float(input("Annual salary: ").strip())
            except ValueError:
                print("Geçersiz maaş.")
                continue
            try:
                with get_connection() as conn:
                    insert_employee(conn, first_name, last_name, annual_salary)
                print("Çalışan eklendi.")
            except sqlite3.Error as e:
                logger.error("Veritabanı hatası: %s", e)
                print(f"Hata: {e}")

        elif choice == "4":
            try:
                emp_id = int(input("Güncellenecek id: ").strip())
            except ValueError:
                print("Geçersiz id.")
                continue
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            try:
                annual_salary = float(input("Annual salary: ").strip())
            except ValueError:
                print("Geçersiz maaş.")
                continue
            try:
                with get_connection() as conn:
                    updated = update_employee(conn, emp_id, first_name, last_name, annual_salary)
                if updated:
                    print("Çalışan güncellendi.")
                else:
                    print("Bu id ile kayıt bulunamadı.")
            except sqlite3.Error as e:
                logger.error("Veritabanı hatası: %s", e)
                print(f"Hata: {e}")

        elif choice == "5":
            try:
                emp_id = int(input("Silinecek id: ").strip())
            except ValueError:
                print("Geçersiz id.")
                continue
            try:
                with get_connection() as conn:
                    deleted = delete_employee(conn, emp_id)
                if deleted:
                    print("Çalışan silindi.")
                else:
                    print("Bu id ile kayıt bulunamadı.")
            except sqlite3.Error as e:
                logger.error("Veritabanı hatası: %s", e)
                print(f"Hata: {e}")

        elif choice == "6":
            print("Çıkılıyor.")
            break

        else:
            print("1-6 arası bir sayı girin.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s [%(name)s] %(message)s",
    )
    main()
