from __future__ import annotations

from datetime import date

from sqlalchemy.exc import IntegrityError

from tasks.exceptions import ValidationError
from tasks.extensions import db
from tasks.models import TASK_STATUSES, Task
from tasks.repositories import SqlAlchemyTaskRepository, TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository | None = None) -> None:
        self._repo = repository or SqlAlchemyTaskRepository()

    def list_tasks(self) -> list[Task]:
        return self._repo.list_all()

    def get_task(self, task_id: int) -> Task | None:
        return self._repo.get_by_id(task_id)

    @staticmethod
    def _validate_dates(start: date | None, end: date | None) -> None:
        if start is not None and end is not None and end < start:
            raise ValidationError("End date cannot be before start date.")

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in TASK_STATUSES:
            raise ValidationError("Invalid status.")

    def create_task(
        self,
        *,
        title: str,
        status: str,
        start_date: date | None,
        end_date: date | None,
    ) -> Task:
        cleaned = (title or "").strip()
        if not cleaned:
            raise ValidationError("Title is required.")
        self._validate_status(status)
        self._validate_dates(start_date, end_date)
        try:
            t = self._repo.create(
                title=cleaned,
                status=status,
                start_date=start_date,
                end_date=end_date,
            )
            db.session.commit()
            return t
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Could not create task (constraint violation).",
            ) from exc

    def update_task(
        self,
        task_id: int,
        *,
        title: str,
        status: str,
        start_date: date | None,
        end_date: date | None,
    ) -> Task:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise ValidationError("Task not found.")
        cleaned = (title or "").strip()
        if not cleaned:
            raise ValidationError("Title is required.")
        self._validate_status(status)
        self._validate_dates(start_date, end_date)
        try:
            t = self._repo.update(
                task,
                title=cleaned,
                status=status,
                start_date=start_date,
                end_date=end_date,
            )
            db.session.commit()
            return t
        except IntegrityError as exc:
            db.session.rollback()
            raise ValidationError(
                "Could not update task (constraint violation).",
            ) from exc

    def delete_task(self, task_id: int) -> None:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise ValidationError("Task not found.")
        self._repo.delete(task)
        db.session.commit()
