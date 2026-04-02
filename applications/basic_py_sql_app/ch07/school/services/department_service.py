from sqlalchemy.exc import IntegrityError

from school.exceptions import ValidationError
from school.extensions import db
from school.models import Department
from school.repositories import (
    DepartmentRepository,
    SqlAlchemyDepartmentRepository,
)


class DepartmentService:
    """İş kuralları: bölüm oluşturma/güncelleme/silme (repository üzerinden)."""

    def __init__(self, repository: DepartmentRepository | None = None) -> None:
        self._repo = repository or SqlAlchemyDepartmentRepository()

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
        try:
            d = self._repo.create(cleaned)
            db.session.commit()
            return d
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Could not create department (constraint violation).",
            ) from exc

    def update_department(self, department_id: int, name: str) -> Department:
        dept = self._repo.get_by_id(department_id)
        if dept is None:
            raise ValidationError("Department not found.")
        cleaned = (name or "").strip()
        if not cleaned:
            raise ValidationError("Department name is required.")
        if self._repo.name_exists(cleaned, exclude_pk=department_id):
            raise ValidationError("A department with this name already exists.")
        try:
            d = self._repo.update(dept, cleaned)
            db.session.commit()
            return d
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Could not update department (constraint violation).",
            ) from exc

    def delete_department(self, department_id: int) -> None:
        dept = self._repo.get_by_id(department_id)
        if dept is None:
            raise ValidationError("Department not found.")
        try:
            self._repo.delete(dept)
            db.session.commit()
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Cannot delete this department because students are assigned to it.",
            ) from exc
