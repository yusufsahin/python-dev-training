from dto.department_dto import DepartmentRequest
from services.department_service import (
    add_department,
    edit_department,
    get_department,
    get_departments,
    remove_department,
    is_valid_department,
)
from services.student_service import initialize_app, load_seed_data


def handle_initialize_app() -> str:
    initialize_app()
    return "Table ready."


def handle_add_department(department_request: DepartmentRequest) -> str:
    if add_department(department_request):
        return "Department inserted."

    return "Department already exists."


def handle_list_departments():
    return get_departments()


def handle_get_department(department_id: int):
    return get_department(department_id)


def handle_is_valid_department(department_id: int) -> bool:
    return is_valid_department(department_id)


def handle_update_department(department_id: int, department_request: DepartmentRequest) -> str:
    result = edit_department(department_id, department_request)
    if result == "updated":
        return "Department updated."
    if result == "conflict":
        return "Department name already exists."

    return "Department not found."


def handle_delete_department(department_id: int) -> str:
    result = remove_department(department_id)
    if result == "deleted":
        return "Department deleted."
    if result == "in_use":
        return "Department is in use by students."

    return "Department not found."


def handle_seed_data() -> str:
    inserted_count = load_seed_data()
    return f"Seed data inserted. Added {inserted_count} students."
