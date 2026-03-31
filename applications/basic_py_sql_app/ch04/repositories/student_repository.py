from db.connection import get_connection
from dto.student_dto import StudentCreate, StudentUpdate
from models.student import Student


def insert_student(student: StudentCreate):
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
                (
                    student.student_number,
                    student.first_name,
                    student.last_name,
                    student.birth_date,
                    student.department_id,
                ),
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
            rows = cur.fetchall()
            return [
                Student(
                    id=row[0],
                    student_number=row[1],
                    first_name=row[2],
                    last_name=row[3],
                    birth_date=row[4],
                    department_name=row[5],
                )
                for row in rows
            ]


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
            row = cur.fetchone()
            if row is None:
                return None

            return Student(
                id=row[0],
                student_number=row[1],
                first_name=row[2],
                last_name=row[3],
                birth_date=row[4],
                department_name=row[5],
            )


def update_student(student_id, student: StudentUpdate):
    sql = """
        UPDATE students
        SET student_number = %s, first_name = %s, last_name = %s, birth_date = %s, department_id = %s
        WHERE id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (
                    student.student_number,
                    student.first_name,
                    student.last_name,
                    student.birth_date,
                    student.department_id,
                    student_id,
                ),
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
