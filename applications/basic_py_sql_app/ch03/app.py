from datetime import datetime

from controllers.department_controller import (
    handle_add_department,
    handle_initialize_app,
    handle_list_departments,
    handle_seed_data,
)
from controllers.student_controller import (
    handle_add_student,
    handle_delete_student,
    handle_get_student,
    handle_list_students,
    handle_update_student,
)
from services.department_service import get_departments, is_valid_department


def parse_birth_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def display_departments(rows):
    if not rows:
        print("No departments found.")
        return

    print("Departments:")
    for row in rows:
        print(f"{row[0]} - {row[1]}")


def display_student(student):
    print(f"ID: {student[0]}")
    print(f"Student Number: {student[1]}")
    print(f"First Name: {student[2]}")
    print(f"Last Name: {student[3]}")
    print(f"Birth Date: {student[4]}")
    print(f"Department: {student[5]}")


def display_students(rows):
    if not rows:
        print("No students found.")
        return

    for student in rows:
        display_student(student)
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

    display_departments(get_departments())

    try:
        department_id = int(input("Department ID: ").strip())
    except ValueError:
        print("Department ID must be a number.")
        return None

    if not is_valid_department(department_id):
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
            print(handle_initialize_app())

        elif choice == "2":
            department_name = input("Department name: ").strip()
            if not department_name:
                print("Department name cannot be empty.")
                continue

            print(handle_add_department(department_name))

        elif choice == "3":
            display_departments(handle_list_departments())

        elif choice == "4":
            student_data = read_student_inputs()
            if student_data is None:
                continue

            print(handle_add_student(student_data))

        elif choice == "5":
            display_students(handle_list_students())

        elif choice == "6":
            student_id = int(input("Student ID: ").strip())
            student = handle_get_student(student_id)
            if student is None:
                print("Student not found.")
            else:
                display_student(student)

        elif choice == "7":
            student_id = int(input("Student ID: ").strip())
            student_data = read_student_inputs()
            if student_data is None:
                continue

            print(handle_update_student(student_id, student_data))

        elif choice == "8":
            student_id = int(input("Student ID: ").strip())
            print(handle_delete_student(student_id))

        elif choice == "9":
            print(handle_seed_data())

        elif choice == "0":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
