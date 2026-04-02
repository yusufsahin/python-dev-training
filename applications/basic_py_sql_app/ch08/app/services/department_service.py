from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import department as dept_repo
from app.exceptions import AppValidationError
from app.models import Department


async def list_departments(session: AsyncSession) -> list[Department]:
    return await dept_repo.list_departments(session)


async def get_department(session: AsyncSession, department_id: int) -> Department | None:
    return await dept_repo.get_department(session, department_id)


async def create_department(session: AsyncSession, name: str) -> Department:
    cleaned = (name or "").strip()
    if not cleaned:
        raise AppValidationError("Department name is required.")
    if await dept_repo.name_exists(session, cleaned):
        raise AppValidationError("A department with this name already exists.")
    try:
        d = await dept_repo.create_department(session, cleaned)
        await session.commit()
        return d
    except IntegrityError as exc:
        await session.rollback()
        raise AppValidationError(
            "Could not create department (constraint violation).",
        ) from exc


async def update_department(session: AsyncSession, department_id: int, name: str) -> Department:
    dept = await dept_repo.get_department(session, department_id)
    if dept is None:
        raise AppValidationError("Department not found.")
    cleaned = (name or "").strip()
    if not cleaned:
        raise AppValidationError("Department name is required.")
    if await dept_repo.name_exists(session, cleaned, exclude_pk=department_id):
        raise AppValidationError("A department with this name already exists.")
    try:
        d = await dept_repo.update_department(session, dept, cleaned)
        await session.commit()
        return d
    except IntegrityError as exc:
        await session.rollback()
        raise AppValidationError(
            "Could not update department (constraint violation).",
        ) from exc


async def delete_department(session: AsyncSession, department_id: int) -> None:
    dept = await dept_repo.get_department(session, department_id)
    if dept is None:
        raise AppValidationError("Department not found.")
    try:
        await dept_repo.delete_department(session, dept)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise AppValidationError(
            "Cannot delete this department because students are assigned to it.",
        ) from exc
