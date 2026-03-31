from dto.student_dto import StudentRequest
from services.student_service import (
    add_student,
    edit_student,
    get_student,
    get_students,
    remove_student,
)


def handle_add_student(student_request: StudentRequest):
    if add_student(student_request):
        return "Student inserted."

    return "Student number already exists."


def handle_list_students():
    return get_students()


def handle_get_student(student_id: int):
    return get_student(student_id)


def handle_update_student(student_id: int, student_request: StudentRequest) -> str:
    if edit_student(student_id, student_request):
        return "Student updated."

    return "Student not found."


def handle_delete_student(student_id: int) -> str:
    if remove_student(student_id):
        return "Student deleted."

    return "Student not found."
