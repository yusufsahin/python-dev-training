from __future__ import annotations

from datetime import date

from motor.motor_asyncio import AsyncIOMotorCollection

from app.constants import TASK_STATUSES
from app.exceptions import AppValidationError
from app.repositories.task import TaskRepository, parse_object_id
from app.schemas.dto import TaskCreateDTO, TaskReadDTO, TaskUpdateDTO

_repo = TaskRepository()


def _validate_dates(start: date | None, end: date | None) -> None:
    if start is not None and end is not None and end < start:
        raise AppValidationError("End date cannot be before start date.")


def _validate_status(status: str) -> None:
    if status not in TASK_STATUSES:
        raise AppValidationError("Invalid status.")


async def list_tasks(coll: AsyncIOMotorCollection) -> list[TaskReadDTO]:
    rows = await _repo.list_all(coll)
    return [TaskReadDTO.from_mongo(d) for d in rows]


async def get_task(coll: AsyncIOMotorCollection, task_id: str) -> TaskReadDTO | None:
    oid = parse_object_id(task_id)
    if oid is None:
        raise AppValidationError("Invalid task id.")
    doc = await _repo.get_by_oid(coll, oid)
    if doc is None:
        return None
    return TaskReadDTO.from_mongo(doc)


async def create_task(coll: AsyncIOMotorCollection, body: TaskCreateDTO) -> TaskReadDTO:
    title = (body.title or "").strip()
    if not title:
        raise AppValidationError("Title is required.")
    _validate_status(body.status)
    _validate_dates(body.start_date, body.end_date)
    doc = await _repo.insert(
        coll,
        title=title,
        status=body.status,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    return TaskReadDTO.from_mongo(doc)


async def update_task(
    coll: AsyncIOMotorCollection,
    task_id: str,
    body: TaskUpdateDTO,
) -> TaskReadDTO:
    oid = parse_object_id(task_id)
    if oid is None:
        raise AppValidationError("Invalid task id.")
    title = (body.title or "").strip()
    if not title:
        raise AppValidationError("Title is required.")
    _validate_status(body.status)
    _validate_dates(body.start_date, body.end_date)
    doc = await _repo.update(
        coll,
        oid,
        title=title,
        status=body.status,
        start_date=body.start_date,
        end_date=body.end_date,
    )
    if doc is None:
        raise AppValidationError("Task not found.")
    return TaskReadDTO.from_mongo(doc)


async def delete_task(coll: AsyncIOMotorCollection, task_id: str) -> None:
    oid = parse_object_id(task_id)
    if oid is None:
        raise AppValidationError("Invalid task id.")
    ok = await _repo.delete(coll, oid)
    if not ok:
        raise AppValidationError("Task not found.")
