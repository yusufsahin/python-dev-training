from datetime import datetime

from db.schema import create_table
from db.seed import seed_data
from repositories.department_repository import (
    department_exists,
    insert_department,
    list_departments,
)
from repositories.student_repository import (
    delete_student,
    get_student_by_id,
    insert_student,
    list_students,
    update_student,
)


def parse_birth_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def display_departments(rows):
    if not rows:
        print("No departments found.")
        return

    print("Departments:")
    for row in rows:
        print(f"{row[0]} - {row[1]}")


def display_student(row):
    print(f"ID: {row[0]}")
    print(f"Student Number: {row[1]}")
    print(f"First Name: {row[2]}")
    print(f"Last Name: {row[3]}")
    print(f"Birth Date: {row[4]}")
    print(f"Department: {row[5]}")


def display_students(rows):
    if not rows:
        print("No students found.")
        return

    for row in rows:
        display_student(row)
        print("-" * 20)


def read_student_inputs():
    student_number = input("Student number: ").strip()
    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()

    if not student_number:
        print("Student number cannot be empty.")
        return None

    if not first_name or not last_name:
        print("First name and last name cannot be empty.")
        return None

    birth_date_text = input("Birth date (YYYY-MM-DD): ").strip()

    try:
        birth_date = parse_birth_date(birth_date_text)
    except ValueError:
        print("Invalid birth date format. Use YYYY-MM-DD.")
        return None

    display_departments(list_departments())

    try:
        department_id = int(input("Department ID: ").strip())
    except ValueError:
        print("Department ID must be a number.")
        return None

    if not department_exists(department_id):
        print("Invalid department ID.")
        return None

    return student_number, first_name, last_name, birth_date, department_id


def menu():
    while True:
        print("\n--- Student App ---")
        print("1 - Create table")
        print("2 - Add department")
        print("3 - List departments")
        print("4 - Insert student")
        print("5 - List students")
        print("6 - Show student by ID")
        print("7 - Update student")
        print("8 - Delete student")
        print("9 - Seed data")
        print("0 - Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            create_table()
            print("Table ready.")

        elif choice == "2":
            department_name = input("Department name: ").strip()
            if not department_name:
                print("Department name cannot be empty.")
                continue

            if insert_department(department_name):
                print("Department inserted.")
            else:
                print("Department already exists.")

        elif choice == "3":
            display_departments(list_departments())

        elif choice == "4":
            student_data = read_student_inputs()
            if student_data is None:
                continue

            if insert_student(*student_data):
                print("Student inserted.")
            else:
                print("Student number already exists.")

        elif choice == "5":
            display_students(list_students())

        elif choice == "6":
            student_id = int(input("Student ID: ").strip())
            student = get_student_by_id(student_id)
            if student is None:
                print("Student not found.")
            else:
                display_student(student)

        elif choice == "7":
            student_id = int(input("Student ID: ").strip())
            student_data = read_student_inputs()
            if student_data is None:
                continue

            if update_student(student_id, *student_data):
                print("Student updated.")
            else:
                print("Student not found.")

        elif choice == "8":
            student_id = int(input("Student ID: ").strip())
            if delete_student(student_id):
                print("Student deleted.")
            else:
                print("Student not found.")

        elif choice == "9":
            inserted_count = seed_data()
            print(f"Seed data inserted. Added {inserted_count} students.")

        elif choice == "0":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
