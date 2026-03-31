from db.connection import get_connection


def insert_student(student_number, first_name, last_name, birth_date, department_id):
    sql = """
        INSERT INTO students (
            student_number, first_name, last_name, birth_date, department_id
        ) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (student_number) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (student_number, first_name, last_name, birth_date, department_id),
            )
            conn.commit()
            return cursor.rowcount > 0


def list_students():
    sql = """
        SELECT
            s.id,
            s.student_number,
            s.first_name,
            s.last_name,
            s.birth_date,
            d.name
        FROM students s
        JOIN departments d ON d.id = s.department_id
        ORDER BY s.id;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


def get_student_by_id(student_id):
    sql = """
        SELECT
            s.id,
            s.student_number,
            s.first_name,
            s.last_name,
            s.birth_date,
            d.name
        FROM students s
        JOIN departments d ON d.id = s.department_id
        WHERE s.id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (student_id,))
            return cur.fetchone()


def update_student(student_id, student_number, first_name, last_name, birth_date, department_id):
    sql = """
        UPDATE students
        SET student_number = %s, first_name = %s, last_name = %s, birth_date = %s, department_id = %s
        WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (student_number, first_name, last_name, birth_date, department_id, student_id),
            )
            conn.commit()
            return cur.rowcount > 0


def delete_student(student_id):
    sql = "DELETE FROM students WHERE id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (student_id,))
            conn.commit()
            return cur.rowcount > 0
