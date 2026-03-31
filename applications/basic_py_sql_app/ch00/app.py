import psycopg

CONN_STR = "dbname=db_app01 user=postgres password=Aloha@2026 host=localhost port=5432"


def create_table():
    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INT NOT NULL
                );
            """)
            conn.commit()


def insert_student(name, age):
    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO students (name, age) VALUES (%s, %s)
            """, (name, age))
            conn.commit()


def list_students():
    sql = "SELECT id, name, age FROM students ORDER BY id;"

    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

            if not rows:
                print("No students found.")
                return

            for row in rows:
                print(f"ID: {row[0]}")
                print(f"Name: {row[1]}")
                print(f"Age: {row[2]}")
                print("-" * 20)


def get_student_by_id(student_id):
    sql = "SELECT id, name, age FROM students WHERE id = %s;"

    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (student_id,))
            row = cur.fetchone()

            if not row:
                print("Student not found.")
                return

            print(f"ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Age: {row[2]}")


def update_student(student_id, name, age):
    sql = "UPDATE students SET name = %s, age = %s WHERE id = %s;"
    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, age, student_id))
            conn.commit()
            print("Student updated.")


def delete_student(student_id):
    sql = "DELETE FROM students WHERE id = %s;"
    with psycopg.connect(CONN_STR) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (student_id,))
            conn.commit()
            print("Student deleted.")


def menu():
    while True:
        print("\n--- Student App ---")
        print("1 - Create table")
        print("2 - Insert student")
        print("3 - List students")
        print("4 - Show student by ID")
        print("5 - Update student")
        print("6 - Delete student")
        print("0 - Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            create_table()
            print("Table ready.")

        elif choice == "2":
            name = input("Name: ").strip()
            age = int(input("Age: ").strip())
            insert_student(name, age)
            print("Student inserted.")

        elif choice == "3":
            list_students()

        elif choice == "4":
            student_id = int(input("Student ID: ").strip())
            get_student_by_id(student_id)

        elif choice == "5":
            student_id = int(input("Student ID: ").strip())
            new_name = input("New name: ").strip()
            new_age = int(input("New age: ").strip())
            update_student(student_id, new_name, new_age)
            print("Student updated.")

        elif choice == "6":
            student_id = int(input("Student ID: ").strip())
            delete_student(student_id)
            print("Student deleted.")

        elif choice == "0":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if _name_ == "_main_":
    menu()
