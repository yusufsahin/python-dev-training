from dependencies import student_service
from dto.student_dto import StudentRequest


def handle_add_student(student_request: StudentRequest):
    if student_service.add_student(student_request):
        return "Student inserted."

    return "Student number already exists."


def handle_list_students():
    return student_service.get_students()


def handle_get_student(student_id: int):
    return student_service.get_student(student_id)


def handle_update_student(student_id: int, student_request: StudentRequest) -> str:
    if student_service.edit_student(student_id, student_request):
        return "Student updated."

    return "Student not found."


def handle_delete_student(student_id: int) -> str:
    if student_service.remove_student(student_id):
        return "Student deleted."

    return "Student not found."
