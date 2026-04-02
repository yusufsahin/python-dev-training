from typing import Literal

from dto.department_dto import DepartmentRequest
from ports import DepartmentRepository


class DepartmentService:
    def __init__(self, repository: DepartmentRepository) -> None:
        self._repository = repository

    def get_departments(self):
        return self._repository.list_departments()

    def get_department(self, department_id: int):
        return self._repository.get_department_by_id(department_id)

    def add_department(self, department_request: DepartmentRequest) -> bool:
        return self._repository.insert_department(department_request.to_create())

    def edit_department(
        self, department_id: int, department_request: DepartmentRequest
    ) -> Literal["updated", "not_found", "conflict"]:
        return self._repository.update_department(department_id, department_request.to_update())

    def remove_department(
        self, department_id: int
    ) -> Literal["deleted", "not_found", "in_use"]:
        return self._repository.delete_department(department_id)

    def is_valid_department(self, department_id: int) -> bool:
        return self._repository.department_exists(department_id)
