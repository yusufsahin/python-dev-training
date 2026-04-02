from db.dialect import SqlDialect, get_dialect
from db.config import load_db_context
from ports import ConnectionFactory


def create_table(
    connect: ConnectionFactory | None = None, dialect: SqlDialect | None = None
) -> None:
    if connect is None or dialect is None:
        ctx = load_db_context()
        factory = connect or ctx.connect
        d = dialect or get_dialect(ctx.backend)
    else:
        factory = connect
        d = dialect

    with factory() as conn:
        with conn.cursor() as cursor:
            cursor.execute(d.students_column_list_sql())
            student_columns = [str(row[0]).lower() for row in cursor.fetchall()]
            expected_columns = [
                "id",
                "student_number",
                "first_name",
                "last_name",
                "birth_date",
                "department_id",
            ]

            if student_columns and student_columns != expected_columns:
                cursor.execute("DROP TABLE IF EXISTS students;")

            cursor.execute(d.ddl_departments())
            cursor.execute(d.ddl_students())
            cursor.execute(d.bootstrap_departments_sql())
            conn.commit()
