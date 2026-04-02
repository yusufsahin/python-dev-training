from school.repositories.department_repository import SqlAlchemyDepartmentRepository
from school.repositories.protocols import DepartmentRepository, StudentRepository
from school.repositories.student_repository import SqlAlchemyStudentRepository

__all__ = [
    "DepartmentRepository",
    "StudentRepository",
    "SqlAlchemyDepartmentRepository",
    "SqlAlchemyStudentRepository",
]
