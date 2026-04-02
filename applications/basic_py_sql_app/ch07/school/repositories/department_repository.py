from sqlalchemy import select

from school.extensions import db
from school.models import Department


class SqlAlchemyDepartmentRepository:
    def list_all(self) -> list[Department]:
        return list(
            db.session.scalars(select(Department).order_by(Department.id)).all(),
        )

    def get_by_id(self, department_id: int) -> Department | None:
        return db.session.get(Department, department_id)

    def create(self, name: str) -> Department:
        d = Department(name=name)
        db.session.add(d)
        db.session.flush()
        return d

    def update(self, department: Department, name: str) -> Department:
        department.name = name
        db.session.add(department)
        db.session.flush()
        return department

    def delete(self, department: Department) -> None:
        db.session.delete(department)
        db.session.flush()

    def name_exists(self, name: str, exclude_pk: int | None = None) -> bool:
        q = select(Department.id).where(Department.name == name)
        if exclude_pk is not None:
            q = q.where(Department.id != exclude_pk)
        return db.session.scalar(q.limit(1)) is not None
