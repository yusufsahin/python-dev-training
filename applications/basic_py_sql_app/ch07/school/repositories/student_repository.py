from sqlalchemy import select
from sqlalchemy.orm import selectinload

from school.extensions import db
from school.models import Department, Student


class SqlAlchemyStudentRepository:
    def list_all(self) -> list[Student]:
        stmt = (
            select(Student)
            .options(selectinload(Student.department))
            .order_by(Student.id)
        )
        return list(db.session.scalars(stmt).all())

    def get_by_id(self, student_id: int) -> Student | None:
        stmt = (
            select(Student)
            .options(selectinload(Student.department))
            .where(Student.id == student_id)
        )
        return db.session.scalars(stmt).first()

    def create(
        self,
        *,
        student_number: str,
        first_name: str,
        last_name: str,
        birth_date,
        department_id: int,
    ) -> Student:
        s = Student(
            student_number=student_number,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            department_id=department_id,
        )
        db.session.add(s)
        db.session.flush()
        return s

    def update(
        self,
        student: Student,
        *,
        student_number: str,
        first_name: str,
        last_name: str,
        birth_date,
        department_id: int,
    ) -> Student:
        student.student_number = student_number
        student.first_name = first_name
        student.last_name = last_name
        student.birth_date = birth_date
        student.department_id = department_id
        db.session.add(student)
        db.session.flush()
        return student

    def delete(self, student: Student) -> None:
        db.session.delete(student)
        db.session.flush()

    def department_exists(self, department_id: int) -> bool:
        return db.session.get(Department, department_id) is not None

    def student_number_exists(
        self, student_number: str, exclude_pk: int | None = None
    ) -> bool:
        q = select(Student.id).where(Student.student_number == student_number)
        if exclude_pk is not None:
            q = q.where(Student.id != exclude_pk)
        return db.session.scalar(q.limit(1)) is not None
