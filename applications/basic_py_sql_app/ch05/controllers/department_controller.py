from dependencies import department_service, student_service
from dto.department_dto import DepartmentRequest


def handle_initialize_app() -> str:
    student_service.initialize_app()
    return "Table ready."


def handle_add_department(department_request: DepartmentRequest) -> str:
    if department_service.add_department(department_request):
        return "Department inserted."

    return "Department already exists."


def handle_list_departments():
    return department_service.get_departments()


def handle_get_department(department_id: int):
    return department_service.get_department(department_id)


def handle_is_valid_department(department_id: int) -> bool:
    return department_service.is_valid_department(department_id)


def handle_update_department(department_id: int, department_request: DepartmentRequest) -> str:
    result = department_service.edit_department(department_id, department_request)
    if result == "updated":
        return "Department updated."
    if result == "conflict":
        return "Department name already exists."

    return "Department not found."


def handle_delete_department(department_id: int) -> str:
    result = department_service.remove_department(department_id)
    if result == "deleted":
        return "Department deleted."
    if result == "in_use":
        return "Department is in use by students."

    return "Department not found."


def handle_seed_data() -> str:
    inserted_count = student_service.load_seed_data()
    return f"Seed data inserted. Added {inserted_count} students."
