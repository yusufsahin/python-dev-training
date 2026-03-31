from db.connection import get_connection


def seed_data():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO departments (name)
                VALUES
                    ('Software Engineering'),
                    ('Electrical Engineering')
                ON CONFLICT (name) DO NOTHING;
            """)

            cur.execute("""
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
            """)
            inserted_count = cur.rowcount
            conn.commit()
            return inserted_count
