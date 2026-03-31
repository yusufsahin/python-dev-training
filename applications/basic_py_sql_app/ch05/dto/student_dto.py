from dataclasses import dataclass
from datetime import date


@dataclass
class StudentCreate:
    student_number: str
    first_name: str
    last_name: str
    birth_date: date
    department_id: int


@dataclass
class StudentUpdate:
    student_number: str
    first_name: str
    last_name: str
    birth_date: date
    department_id: int


@dataclass
class StudentRequest:
    student_number: str
    first_name: str
    last_name: str
    birth_date: date
    department_id: int

    def to_create(self) -> StudentCreate:
        return StudentCreate(
            student_number=self.student_number,
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            department_id=self.department_id,
        )

    def to_update(self) -> StudentUpdate:
        return StudentUpdate(
            student_number=self.student_number,
            first_name=self.first_name,
            last_name=self.last_name,
            birth_date=self.birth_date,
            department_id=self.department_id,
        )
