from datetime import datetime

from controllers.department_controller import (
    handle_add_department,
    handle_delete_department,
    handle_get_department,
    handle_initialize_app,
    handle_is_valid_department,
    handle_list_departments,
    handle_seed_data,
    handle_update_department,
)
from controllers.student_controller import (
    handle_add_student,
    handle_delete_student,
    handle_get_student,
    handle_list_students,
    handle_update_student,
)
from dto.department_dto import DepartmentRequest
from dto.student_dto import StudentRequest


def parse_birth_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def display_departments(rows):
    if not rows:
        print("No departments found.")
        return

    print("Departments:")
    for department in rows:
        print(f"{department.id} - {department.name}")


def display_student(student):
    print(f"ID: {student.id}")
    print(f"Student Number: {student.student_number}")
    print(f"First Name: {student.first_name}")
    print(f"Last Name: {student.last_name}")
    print(f"Birth Date: {student.birth_date}")
    print(f"Department: {student.department_name}")


def display_department(department):
    print(f"ID: {department.id}")
    print(f"Name: {department.name}")


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

    display_departments(handle_list_departments())

    try:
        department_id = int(input("Department ID: ").strip())
    except ValueError:
        print("Department ID must be a number.")
        return None

    if not handle_is_valid_department(department_id):
        print("Invalid department ID.")
        return None

    return StudentRequest(
        student_number=student_number,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        department_id=department_id,
    )


def menu():
    while True:
        print("\n--- Student App ---")
        print("1 - Create table")
        print("2 - Add department")
        print("3 - List departments")
        print("4 - Show department by ID")
        print("5 - Update department")
        print("6 - Delete department")
        print("7 - Insert student")
        print("8 - List students")
        print("9 - Show student by ID")
        print("10 - Update student")
        print("11 - Delete student")
        print("12 - Seed data")
        print("0 - Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            print(handle_initialize_app())

        elif choice == "2":
            department_name = input("Department name: ").strip()
            if not department_name:
                print("Department name cannot be empty.")
                continue

            department_request = DepartmentRequest(name=department_name)
            print(handle_add_department(department_request))

        elif choice == "3":
            display_departments(handle_list_departments())

        elif choice == "4":
            department_id = int(input("Department ID: ").strip())
            department = handle_get_department(department_id)
            if department is None:
                print("Department not found.")
            else:
                display_department(department)

        elif choice == "5":
            department_id = int(input("Department ID: ").strip())
            department_name = input("New department name: ").strip()
            if not department_name:
                print("Department name cannot be empty.")
                continue

            department_request = DepartmentRequest(name=department_name)
            print(handle_update_department(department_id, department_request))

        elif choice == "6":
            department_id = int(input("Department ID: ").strip())
            print(handle_delete_department(department_id))

        elif choice == "7":
            student_data = read_student_inputs()
            if student_data is None:
                continue

            print(handle_add_student(student_data))

        elif choice == "8":
            display_students(handle_list_students())

        elif choice == "9":
            student_id = int(input("Student ID: ").strip())
            student = handle_get_student(student_id)
            if student is None:
                print("Student not found.")
            else:
                display_student(student)

        elif choice == "10":
            student_id = int(input("Student ID: ").strip())
            student_data = read_student_inputs()
            if student_data is None:
                continue

            print(handle_update_student(student_id, student_data))

        elif choice == "11":
            student_id = int(input("Student ID: ").strip())
            print(handle_delete_student(student_id))

        elif choice == "12":
            print(handle_seed_data())

        elif choice == "0":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
