from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Department


async def list_departments(session: AsyncSession) -> list[Department]:
    r = await session.execute(select(Department).order_by(Department.id))
    return list(r.scalars().all())


async def get_department(session: AsyncSession, department_id: int) -> Department | None:
    return await session.get(Department, department_id)


async def name_exists(
    session: AsyncSession, name: str, *, exclude_pk: int | None = None
) -> bool:
    q = select(Department.id).where(Department.name == name)
    if exclude_pk is not None:
        q = q.where(Department.id != exclude_pk)
    r = await session.execute(q.limit(1))
    return r.scalar_one_or_none() is not None


async def create_department(session: AsyncSession, name: str) -> Department:
    d = Department(name=name)
    session.add(d)
    await session.flush()
    await session.refresh(d)
    return d


async def update_department(session: AsyncSession, dept: Department, name: str) -> Department:
    dept.name = name
    session.add(dept)
    await session.flush()
    await session.refresh(dept)
    return dept


async def delete_department(session: AsyncSession, dept: Department) -> None:
    await session.delete(dept)
    await session.flush()
