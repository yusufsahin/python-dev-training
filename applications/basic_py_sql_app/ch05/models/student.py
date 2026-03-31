from dataclasses import dataclass
from datetime import date


@dataclass
class Student:
    id: int
    student_number: str
    first_name: str
    last_name: str
    birth_date: date
    department_name: str
