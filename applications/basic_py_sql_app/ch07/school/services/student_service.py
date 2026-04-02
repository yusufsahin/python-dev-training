from sqlalchemy.exc import IntegrityError

from school.exceptions import ValidationError
from school.extensions import db
from school.models import Student
from school.repositories import SqlAlchemyStudentRepository, StudentRepository


class StudentService:
    """İş kuralları: öğrenci CRUD (repository üzerinden)."""

    def __init__(self, repository: StudentRepository | None = None) -> None:
        self._repo = repository or SqlAlchemyStudentRepository()

    def list_students(self) -> list[Student]:
        return self._repo.list_all()

    def get_student(self, student_id: int) -> Student | None:
        return self._repo.get_by_id(student_id)

    def create_student(
        self,
        *,
        student_number: str,
        first_name: str,
        last_name: str,
        birth_date,
        department_id: int,
    ) -> Student:
        sn = (student_number or "").strip()
        fn = (first_name or "").strip()
        ln = (last_name or "").strip()
        if not sn or not fn or not ln:
            raise ValidationError(
                "Student number, first name and last name are required.",
            )
        if not self._repo.department_exists(department_id):
            raise ValidationError("Invalid department.")
        if self._repo.student_number_exists(sn):
            raise ValidationError("This student number is already in use.")
        try:
            s = self._repo.create(
                student_number=sn,
                first_name=fn,
                last_name=ln,
                birth_date=birth_date,
                department_id=department_id,
            )
            db.session.commit()
            return s
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Could not create student (constraint violation).",
            ) from exc

    def update_student(
        self,
        student_id: int,
        *,
        student_number: str,
        first_name: str,
        last_name: str,
        birth_date,
        department_id: int,
    ) -> Student:
        student = self._repo.get_by_id(student_id)
        if student is None:
            raise ValidationError("Student not found.")
        sn = (student_number or "").strip()
        fn = (first_name or "").strip()
        ln = (last_name or "").strip()
        if not sn or not fn or not ln:
            raise ValidationError(
                "Student number, first name and last name are required.",
            )
        if not self._repo.department_exists(department_id):
            raise ValidationError("Invalid department.")
        if self._repo.student_number_exists(sn, exclude_pk=student_id):
            raise ValidationError("This student number is already in use.")
        try:
            s = self._repo.update(
                student,
                student_number=sn,
                first_name=fn,
                last_name=ln,
                birth_date=birth_date,
                department_id=department_id,
            )
            db.session.commit()
            return s
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Could not update student (constraint violation).",
            ) from exc

    def delete_student(self, student_id: int) -> None:
        student = self._repo.get_by_id(student_id)
        if student is None:
            raise ValidationError("Student not found.")
        self._repo.delete(student)
        db.session.commit()
