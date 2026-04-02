from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import student as st_repo
from app.exceptions import AppValidationError
from app.models import Student


async def list_students(session: AsyncSession) -> list[Student]:
    return await st_repo.list_students(session)


async def get_student(session: AsyncSession, student_id: int) -> Student | None:
    return await st_repo.get_student(session, student_id)


async def create_student(
    session: AsyncSession,
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
        raise AppValidationError(
            "Student number, first name and last name are required.",
        )
    if not await st_repo.department_exists(session, department_id):
        raise AppValidationError("Invalid department.")
    if await st_repo.student_number_exists(session, sn):
        raise AppValidationError("This student number is already in use.")
    try:
        s = await st_repo.create_student(
            session,
            student_number=sn,
            first_name=fn,
            last_name=ln,
            birth_date=birth_date,
            department_id=department_id,
        )
        await session.commit()
        return s
    except IntegrityError as exc:
        await session.rollback()
        raise AppValidationError(
            "Could not create student (constraint violation).",
        ) from exc


async def update_student(
    session: AsyncSession,
    student_id: int,
    *,
    student_number: str,
    first_name: str,
    last_name: str,
    birth_date,
    department_id: int,
) -> Student:
    student = await st_repo.get_student(session, student_id)
    if student is None:
        raise AppValidationError("Student not found.")
    sn = (student_number or "").strip()
    fn = (first_name or "").strip()
    ln = (last_name or "").strip()
    if not sn or not fn or not ln:
        raise AppValidationError(
            "Student number, first name and last name are required.",
        )
    if not await st_repo.department_exists(session, department_id):
        raise AppValidationError("Invalid department.")
    if await st_repo.student_number_exists(session, sn, exclude_pk=student_id):
        raise AppValidationError("This student number is already in use.")
    try:
        s = await st_repo.update_student(
            session,
            student,
            student_number=sn,
            first_name=fn,
            last_name=ln,
            birth_date=birth_date,
            department_id=department_id,
        )
        await session.commit()
        return s
    except IntegrityError as exc:
        await session.rollback()
        raise AppValidationError(
            "Could not update student (constraint violation).",
        ) from exc


async def delete_student(session: AsyncSession, student_id: int) -> None:
    student = await st_repo.get_student(session, student_id)
    if student is None:
        raise AppValidationError("Student not found.")
    await st_repo.delete_student(session, student)
    await session.commit()
