"""PostgreSQL ve MySQL için DDL / DML farklarını soyutlar."""

from typing import Protocol

from db.backend_kind import DbBackend


class SqlDialect(Protocol):
    def students_column_list_sql(self) -> str: ...
    def ddl_departments(self) -> str: ...
    def ddl_students(self) -> str: ...
    def bootstrap_departments_sql(self) -> str: ...
    def seed_extra_departments_sql(self) -> str: ...
    def seed_students_sql(self) -> str: ...
    def insert_department_ignore_sql(self) -> str: ...
    def insert_student_ignore_sql(self) -> str: ...


class PostgresDialect:
    def students_column_list_sql(self) -> str:
        return """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'students'
            ORDER BY ordinal_position;
        """

    def ddl_departments(self) -> str:
        return """
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            );
        """

    def ddl_students(self) -> str:
        return """
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                student_number VARCHAR(20) NOT NULL UNIQUE,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                birth_date DATE NOT NULL,
                department_id INT NOT NULL REFERENCES departments(id)
            );
        """

    def bootstrap_departments_sql(self) -> str:
        return """
            INSERT INTO departments (name)
            VALUES
                ('Computer Science'),
                ('Mathematics'),
                ('Physics')
            ON CONFLICT (name) DO NOTHING;
        """

    def seed_extra_departments_sql(self) -> str:
        return """
            INSERT INTO departments (name)
            VALUES
                ('Software Engineering'),
                ('Electrical Engineering')
            ON CONFLICT (name) DO NOTHING;
        """

    def seed_students_sql(self) -> str:
        return """
            INSERT INTO students (
                student_number, first_name, last_name, birth_date, department_id
            )
            SELECT * FROM (
                VALUES
                    ('2024001', 'Ahmet', 'Yilmaz', DATE '2003-05-14',
                        (SELECT id FROM departments WHERE name = 'Computer Science')),
                    ('2024002', 'Ayse', 'Demir', DATE '2002-11-03',
                        (SELECT id FROM departments WHERE name = 'Mathematics')),
                    ('2024003', 'Mehmet', 'Kaya', DATE '2004-01-22',
                        (SELECT id FROM departments WHERE name = 'Physics')),
                    ('2024004', 'Elif', 'Acar', DATE '2003-08-09',
                        (SELECT id FROM departments WHERE name = 'Software Engineering'))
            ) AS seed_students(student_number, first_name, last_name, birth_date, department_id)
            ON CONFLICT (student_number) DO NOTHING;
        """

    def insert_department_ignore_sql(self) -> str:
        return """
            INSERT INTO departments (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """

    def insert_student_ignore_sql(self) -> str:
        return """
            INSERT INTO students (
                student_number, first_name, last_name, birth_date, department_id
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (student_number) DO NOTHING;
        """


class MysqlDialect:
    def students_column_list_sql(self) -> str:
        return """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = DATABASE() AND table_name = 'students'
            ORDER BY ordinal_position;
        """

    def ddl_departments(self) -> str:
        return """
            CREATE TABLE IF NOT EXISTS departments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            );
        """

    def ddl_students(self) -> str:
        return """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_number VARCHAR(20) NOT NULL UNIQUE,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                birth_date DATE NOT NULL,
                department_id INT NOT NULL,
                CONSTRAINT fk_students_department
                    FOREIGN KEY (department_id) REFERENCES departments(id)
            );
        """

    def bootstrap_departments_sql(self) -> str:
        return """
            INSERT IGNORE INTO departments (name) VALUES
                ('Computer Science'),
                ('Mathematics'),
                ('Physics');
        """

    def seed_extra_departments_sql(self) -> str:
        return """
            INSERT IGNORE INTO departments (name) VALUES
                ('Software Engineering'),
                ('Electrical Engineering');
        """

    def seed_students_sql(self) -> str:
        # MySQL: LIMIT her SELECT için ayrı parantez içinde olmalı; aksi halde tüm UNION tek satıra düşer.
        # INSERT…(SELECT) UNION sözdizimi geçersiz; bu yüzden dışarıda SELECT … FROM (…) AS sub.
        return """
            INSERT IGNORE INTO students (
                student_number, first_name, last_name, birth_date, department_id
            )
            SELECT
                student_number, first_name, last_name, birth_date, department_id
            FROM (
                (SELECT
                    '2024001' AS student_number,
                    'Ahmet' AS first_name,
                    'Yilmaz' AS last_name,
                    CAST('2003-05-14' AS DATE) AS birth_date,
                    id AS department_id
                 FROM departments WHERE name = 'Computer Science' LIMIT 1)
                UNION ALL
                (SELECT
                    '2024002', 'Ayse', 'Demir', CAST('2002-11-03' AS DATE), id
                 FROM departments WHERE name = 'Mathematics' LIMIT 1)
                UNION ALL
                (SELECT
                    '2024003', 'Mehmet', 'Kaya', CAST('2004-01-22' AS DATE), id
                 FROM departments WHERE name = 'Physics' LIMIT 1)
                UNION ALL
                (SELECT
                    '2024004', 'Elif', 'Acar', CAST('2003-08-09' AS DATE), id
                 FROM departments WHERE name = 'Software Engineering' LIMIT 1)
            ) AS seed_rows;
        """

    def insert_department_ignore_sql(self) -> str:
        return "INSERT IGNORE INTO departments (name) VALUES (%s);"

    def insert_student_ignore_sql(self) -> str:
        return """
            INSERT IGNORE INTO students (
                student_number, first_name, last_name, birth_date, department_id
            ) VALUES (%s, %s, %s, %s, %s);
        """


_DIALECTS: dict[DbBackend, SqlDialect] = {
    DbBackend.POSTGRESQL: PostgresDialect(),
    DbBackend.MYSQL: MysqlDialect(),
}


def get_dialect(backend: DbBackend) -> SqlDialect:
    return _DIALECTS[backend]
