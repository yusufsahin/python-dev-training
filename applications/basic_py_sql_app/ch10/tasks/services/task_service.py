from __future__ import annotations

from datetime import date

from mongoengine.errors import ValidationError as MongoValidationError

from tasks.exceptions import ValidationError
from tasks.models import TASK_STATUSES, Task
from tasks.repositories import MongoTaskRepository, TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository | None = None) -> None:
        self._repo = repository or MongoTaskRepository()

    def list_tasks(self) -> list[Task]:
        return self._repo.list_all()

    def get_task(self, task_id: str) -> Task | None:
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
            return self._repo.create(
                title=cleaned,
                status=status,
                start_date=start_date,
                end_date=end_date,
            )
        except MongoValidationError as exc:
            raise ValidationError(str(exc)) from exc

    def update_task(
        self,
        task_id: str,
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
            return self._repo.update(
                task,
                title=cleaned,
                status=status,
                start_date=start_date,
                end_date=end_date,
            )
        except (MongoValidationError, OperationError) as exc:
            raise ValidationError(str(exc)) from exc

    def delete_task(self, task_id: str) -> None:
        task = self._repo.get_by_id(task_id)
        if task is None:
            raise ValidationError("Task not found.")
        self._repo.delete(task)
