from db.dialect import SqlDialect, get_dialect
from db.config import load_db_context
from dto.student_dto import StudentCreate, StudentUpdate
from models.student import Student
from ports import ConnectionFactory


class SqlStudentRepository:
    def __init__(
        self,
        connect: ConnectionFactory | None = None,
        dialect: SqlDialect | None = None,
    ) -> None:
        if connect is None or dialect is None:
            ctx = load_db_context()
            self._connect = connect or ctx.connect
            self._dialect = dialect or get_dialect(ctx.backend)
        else:
            self._connect = connect
            self._dialect = dialect

    def insert_student(self, student: StudentCreate) -> bool:
        sql = self._dialect.insert_student_ignore_sql()

        with self._connect() as conn:
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

    def list_students(self) -> list[Student]:
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

        with self._connect() as conn:
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

    def get_student_by_id(self, student_id: int) -> Student | None:
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

        with self._connect() as conn:
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

    def update_student(self, student_id: int, student: StudentUpdate) -> bool:
        sql = """
            UPDATE students
            SET student_number = %s, first_name = %s, last_name = %s, birth_date = %s, department_id = %s
            WHERE id = %s;
        """

        with self._connect() as conn:
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

    def delete_student(self, student_id: int) -> bool:
        sql = "DELETE FROM students WHERE id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (student_id,))
                conn.commit()
                return cur.rowcount > 0
