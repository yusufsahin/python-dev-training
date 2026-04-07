from __future__ import annotations

from typing import Protocol

from tasks.models import Task


class TaskRepository(Protocol):
    def list_all(self) -> list[Task]: ...

    def get_by_id(self, task_id: str) -> Task | None: ...

    def create(
        self,
        *,
        title: str,
        status: str,
        start_date,
        end_date,
    ) -> Task: ...

    def update(
        self,
        task: Task,
        *,
        title: str,
        status: str,
        start_date,
        end_date,
    ) -> Task: ...

    def delete(self, task: Task) -> None: ...
