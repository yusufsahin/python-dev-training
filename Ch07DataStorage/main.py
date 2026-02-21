import sqlite3
DB_PATH="myDB.sqlite3"

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_table(conn):
    cur = conn.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                 salary REAL)
            """)
        conn.commit()
    finally:
        cur.close()
def insert_employee(conn,name,salary):
    cur = conn.cursor()
    try:
        cur.execute("""
         INSERT INTO employees(name, salary) VALUES (?, ?)
        """, (name, salary))
        conn.commit()
    finally:
        cur.close()

def fetch_employees(conn):
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, salary FROM employees")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    finally:
        cur.close()
def main():
    conn = create_connection()
    try:
        cur = conn.cursor()
        try:
            cur.execute("SELECT sqlite_version();")
            db_version = cur.fetchone()
            print(f"SQLite version: {db_version[0]}")
        finally:
            cur.close()

        create_table(conn)
        insert_employee(conn, "John Doe", 50000)
        insert_employee(conn, "Jane Doe", 60000)

        fetch_employees(conn)

    finally:
        conn.close()

if __name__ == "__main__":
    main()