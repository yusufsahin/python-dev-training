"""Async seed — boş DB için demo veri."""

import asyncio
import sys
from datetime import date

from sqlalchemy import func, select

from app.database import async_session_maker
from app.exceptions import AppValidationError
from app.models import Department
from app.services import department_service, student_service


async def seed_demo_data() -> None:
    async with async_session_maker() as session:
        for name in ["Computer Science", "Mathematics", "Physics", "Software Engineering"]:
            try:
                await department_service.create_department(session, name)
                print(f"Department: {name}")
            except AppValidationError:
                print(f"Department exists: {name}")

        async def dept_id(n: str) -> int:
            rows = await department_service.list_departments(session)
            for d in rows:
                if d.name == n:
                    return d.id
            raise RuntimeError(f"missing department {n}")

        samples = [
            ("2024001", "Ahmet", "Yilmaz", date(2003, 5, 14), "Computer Science"),
            ("2024002", "Ayse", "Demir", date(2002, 11, 3), "Mathematics"),
            ("2024003", "Mehmet", "Kaya", date(2004, 1, 22), "Physics"),
        ]
        for sn, fn, ln, bd, dname in samples:
            try:
                await student_service.create_student(
                    session,
                    student_number=sn,
                    first_name=fn,
                    last_name=ln,
                    birth_date=bd,
                    department_id=await dept_id(dname),
                )
                print(f"Student: {sn}")
            except AppValidationError as exc:
                print(f"Skip {sn}: {exc.messages[0]}")

    print("Seed finished.")


async def ensure_initial_data() -> None:
    async with async_session_maker() as session:
        n = await session.scalar(select(func.count()).select_from(Department))
        if n and n > 0:
            print("Seed skipped: database already has departments.")
            return
    print("Running initial seed…")
    await seed_demo_data()
    print("Initial data ready.")


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "seed"
    if cmd == "ensure":
        asyncio.run(ensure_initial_data())
    else:
        asyncio.run(seed_demo_data())


if __name__ == "__main__":
    main()
