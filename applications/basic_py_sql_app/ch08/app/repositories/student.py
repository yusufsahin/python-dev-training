from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Department, Student


async def list_students(session: AsyncSession) -> list[Student]:
    stmt = (
        select(Student)
        .options(selectinload(Student.department))
        .order_by(Student.id)
    )
    r = await session.execute(stmt)
    return list(r.scalars().all())


async def get_student(session: AsyncSession, student_id: int) -> Student | None:
    stmt = (
        select(Student)
        .options(selectinload(Student.department))
        .where(Student.id == student_id)
    )
    r = await session.execute(stmt)
    return r.scalar_one_or_none()


async def department_exists(session: AsyncSession, department_id: int) -> bool:
    return await session.get(Department, department_id) is not None


async def student_number_exists(
    session: AsyncSession, student_number: str, *, exclude_pk: int | None = None
) -> bool:
    q = select(Student.id).where(Student.student_number == student_number)
    if exclude_pk is not None:
        q = q.where(Student.id != exclude_pk)
    r = await session.execute(q.limit(1))
    return r.scalar_one_or_none() is not None


async def create_student(
    session: AsyncSession,
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
    session.add(s)
    await session.flush()
    await session.refresh(s)
    stmt = (
        select(Student)
        .options(selectinload(Student.department))
        .where(Student.id == s.id)
    )
    r2 = await session.execute(stmt)
    return r2.scalar_one()


async def update_student(
    session: AsyncSession,
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
    session.add(student)
    await session.flush()
    await session.refresh(student)
    stmt = (
        select(Student)
        .options(selectinload(Student.department))
        .where(Student.id == student.id)
    )
    r2 = await session.execute(stmt)
    return r2.scalar_one()


async def delete_student(session: AsyncSession, student: Student) -> None:
    await session.delete(student)
    await session.flush()
