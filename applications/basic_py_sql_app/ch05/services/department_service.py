from dto.department_dto import DepartmentRequest
from repositories.department_repository import (
    delete_department,
    department_exists,
    get_department_by_id,
    insert_department,
    list_departments,
    update_department,
)


def get_departments():
    return list_departments()


def get_department(department_id: int):
    return get_department_by_id(department_id)


def add_department(department_request: DepartmentRequest) -> bool:
    return insert_department(department_request.to_create())


def edit_department(department_id: int, department_request: DepartmentRequest) -> str:
    return update_department(department_id, department_request.to_update())


def remove_department(department_id: int) -> str:
    return delete_department(department_id)


def is_valid_department(department_id):
    return department_exists(department_id)
