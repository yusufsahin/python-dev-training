from contextlib import nullcontext
from datetime import date

from db.backend_kind import DbBackend
from db.dialect import get_dialect
from dto.department_dto import DepartmentRequest
from dto.student_dto import StudentRequest
from models.department import Department
from models.student import Student
from services.department_service import DepartmentService
from services.student_service import StudentService


def _noop_connect():
    return nullcontext(None)


class FakeStudentRepository:
    def __init__(self) -> None:
        self.rows = [
            Student(1, "S1", "Ada", "Lovelace", date(1815, 12, 10), "Mathematics"),
        ]

    def list_students(self):
        return list(self.rows)

    def get_student_by_id(self, student_id: int):
        for r in self.rows:
            if r.id == student_id:
                return r
        return None

    def insert_student(self, student) -> bool:
        return True

    def update_student(self, student_id: int, student) -> bool:
        return student_id == 1

    def delete_student(self, student_id: int) -> bool:
        return student_id == 1


class FakeDepartmentRepository:
    def __init__(self) -> None:
        self.rows = [Department(1, "Physics")]

    def list_departments(self):
        return list(self.rows)

    def get_department_by_id(self, department_id: int):
        for r in self.rows:
            if r.id == department_id:
                return r
        return None

    def insert_department(self, department) -> bool:
        return True

    def update_department(self, department_id: int, department):
        return "updated"

    def delete_department(self, department_id: int):
        return "deleted"

    def department_exists(self, department_id: int) -> bool:
        return department_id == 1


def test_student_service_list_and_get():
    dialect = get_dialect(DbBackend.POSTGRESQL)
    svc = StudentService(FakeStudentRepository(), _noop_connect, dialect)
    assert len(svc.get_students()) == 1
    assert svc.get_student(1) is not None
    assert svc.get_student(99) is None


def test_student_service_add():
    dialect = get_dialect(DbBackend.POSTGRESQL)
    svc = StudentService(FakeStudentRepository(), _noop_connect, dialect)
    req = StudentRequest(
        student_number="X",
        first_name="A",
        last_name="B",
        birth_date=date(2000, 1, 1),
        department_id=1,
    )
    assert svc.add_student(req) is True


def test_department_service_crud_flow():
    svc = DepartmentService(FakeDepartmentRepository())
    assert svc.get_department(1).name == "Physics"
    assert svc.is_valid_department(1) is True
    assert svc.is_valid_department(2) is False
    assert svc.add_department(DepartmentRequest(name="New")) is True
    assert svc.edit_department(1, DepartmentRequest(name="Renamed")) == "updated"
    assert svc.remove_department(1) == "deleted"
