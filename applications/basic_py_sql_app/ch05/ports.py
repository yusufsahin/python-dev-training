from typing import Any, ContextManager, Literal, Protocol

from dto.department_dto import DepartmentCreate, DepartmentUpdate
from dto.student_dto import StudentCreate, StudentUpdate
from models.department import Department
from models.student import Student


class ConnectionFactory(Protocol):
    def __call__(self) -> ContextManager[Any]: ...


class StudentRepository(Protocol):
    def insert_student(self, student: StudentCreate) -> bool: ...

    def list_students(self) -> list[Student]: ...

    def get_student_by_id(self, student_id: int) -> Student | None: ...

    def update_student(self, student_id: int, student: StudentUpdate) -> bool: ...

    def delete_student(self, student_id: int) -> bool: ...


class DepartmentRepository(Protocol):
    def list_departments(self) -> list[Department]: ...

    def insert_department(self, department: DepartmentCreate) -> bool: ...

    def get_department_by_id(self, department_id: int) -> Department | None: ...

    def update_department(
        self, department_id: int, department: DepartmentUpdate
    ) -> Literal["updated", "not_found", "conflict"]: ...

    def delete_department(
        self, department_id: int
    ) -> Literal["deleted", "not_found", "in_use"]: ...

    def department_exists(self, department_id: int) -> bool: ...
