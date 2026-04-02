from school.repositories.department_repository import DjangoDepartmentRepository
from school.repositories.protocols import DepartmentRepository, StudentRepository
from school.repositories.student_repository import DjangoStudentRepository

__all__ = [
    "DepartmentRepository",
    "StudentRepository",
    "DjangoDepartmentRepository",
    "DjangoStudentRepository",
]
