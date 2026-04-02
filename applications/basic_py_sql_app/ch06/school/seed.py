"""Demo bölüm ve öğrenci verisi — management komutları ve entrypoint tarafından kullanılır."""

from __future__ import annotations

import sys
from datetime import date
from typing import IO, Any

from django.core.exceptions import ValidationError

from school.services import DepartmentService, StudentService


def seed_demo_data(stdout: IO[str] | Any | None = None) -> None:
    """Bölümleri ve örnek öğrencileri oluşturur (aynı kayıtlar servis kurallarıyla atlanır)."""
    out = stdout if stdout is not None else sys.stdout
    write = out.write

    dept_svc = DepartmentService()
    st_svc = StudentService()

    for name in ["Computer Science", "Mathematics", "Physics", "Software Engineering"]:
        try:
            dept_svc.create_department(name)
            write(f"Department: {name}\n")
        except ValidationError:
            write(f"Department exists: {name}\n")

    def dept_id(n: str) -> int:
        for d in dept_svc.list_departments():
            if d.name == n:
                return d.pk
        raise RuntimeError(f"missing department {n}")

    samples = [
        ("2024001", "Ahmet", "Yilmaz", date(2003, 5, 14), "Computer Science"),
        ("2024002", "Ayse", "Demir", date(2002, 11, 3), "Mathematics"),
        ("2024003", "Mehmet", "Kaya", date(2004, 1, 22), "Physics"),
    ]
    for sn, fn, ln, bd, dname in samples:
        try:
            st_svc.create_student(
                student_number=sn,
                first_name=fn,
                last_name=ln,
                birth_date=bd,
                department_id=dept_id(dname),
            )
            write(f"Student: {sn}\n")
        except ValidationError as exc:
            write(f"Skip {sn}: {exc.messages[0]}\n")

    write("Seed finished.\n")
