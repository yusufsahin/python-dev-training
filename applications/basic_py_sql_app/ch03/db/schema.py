from db.connection import get_connection


def create_table():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'students'
                ORDER BY ordinal_position;
            """)
            student_columns = [row[0] for row in cursor.fetchall()]
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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    student_number VARCHAR(20) NOT NULL UNIQUE,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    birth_date DATE NOT NULL,
                    department_id INT NOT NULL REFERENCES departments(id)
                );
            """)
            cursor.execute("""
                INSERT INTO departments (name)
                VALUES
                    ('Computer Science'),
                    ('Mathematics'),
                    ('Physics')
                ON CONFLICT (name) DO NOTHING;
            """)
            conn.commit()
