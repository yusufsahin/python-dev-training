from services.student_service import (
    add_student,
    edit_student,
    get_student,
    get_students,
    remove_student,
)


def handle_add_student(student_data):
    if add_student(*student_data):
        return "Student inserted."

    return "Student number already exists."


def handle_list_students():
    return get_students()


def handle_get_student(student_id):
    return get_student(student_id)


def handle_update_student(student_id, student_data):
    if edit_student(student_id, *student_data):
        return "Student updated."

    return "Student not found."


def handle_delete_student(student_id):
    if remove_student(student_id):
        return "Student deleted."

    return "Student not found."
