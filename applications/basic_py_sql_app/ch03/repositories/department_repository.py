from db.connection import get_connection


def list_departments():
    sql = "SELECT id, name FROM departments ORDER BY id;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


def insert_department(name):
    sql = """
        INSERT INTO departments (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name,))
            conn.commit()
            return cur.rowcount > 0


def department_exists(department_id):
    sql = "SELECT 1 FROM departments WHERE id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (department_id,))
            return cur.fetchone() is not None
