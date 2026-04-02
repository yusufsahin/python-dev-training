from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError

from school.models import Department
from school.repositories import (
    DepartmentRepository,
    DjangoDepartmentRepository,
)


class DepartmentService:
    """İş kuralları: bölüm oluşturma/güncelleme/silme (repository üzerinden)."""

    def __init__(self, repository: DepartmentRepository | None = None) -> None:
        self._repo = repository or DjangoDepartmentRepository()

    def list_departments(self) -> list[Department]:
        return self._repo.list_all()

    def get_department(self, department_id: int) -> Department | None:
        return self._repo.get_by_id(department_id)

    def create_department(self, name: str) -> Department:
        cleaned = (name or "").strip()
        if not cleaned:
            raise ValidationError("Department name is required.")
        if self._repo.name_exists(cleaned):
            raise ValidationError("A department with this name already exists.")
        return self._repo.create(cleaned)

    def update_department(self, department_id: int, name: str) -> Department:
        dept = self._repo.get_by_id(department_id)
        if dept is None:
            raise ValidationError("Department not found.")
        cleaned = (name or "").strip()
        if not cleaned:
            raise ValidationError("Department name is required.")
        if self._repo.name_exists(cleaned, exclude_pk=department_id):
            raise ValidationError("A department with this name already exists.")
        return self._repo.update(dept, cleaned)

    def delete_department(self, department_id: int) -> None:
        dept = self._repo.get_by_id(department_id)
        if dept is None:
            raise ValidationError("Department not found.")
        try:
            self._repo.delete(dept)
        except ProtectedError as exc:
            raise ValidationError(
                "Cannot delete this department because students are assigned to it.",
            ) from exc
