from __future__ import annotations

from sqlalchemy import select

from tasks.extensions import db
from tasks.models import Task


class SqlAlchemyTaskRepository:
    def list_all(self) -> list[Task]:
        return list(
            db.session.scalars(select(Task).order_by(Task.id.desc())).all(),
        )

    def get_by_id(self, task_id: int) -> Task | None:
        return db.session.get(Task, task_id)

    def create(
        self,
        *,
        title: str,
        status: str,
        start_date,
        end_date,
    ) -> Task:
        t = Task(
            title=title,
            status=status,
            start_date=start_date,
            end_date=end_date,
        )
        db.session.add(t)
        db.session.flush()
        return t

    def update(
        self,
        task: Task,
        *,
        title: str,
        status: str,
        start_date,
        end_date,
    ) -> Task:
        task.title = title
        task.status = status
        task.start_date = start_date
        task.end_date = end_date
        db.session.add(task)
        db.session.flush()
        return task

    def delete(self, task: Task) -> None:
        db.session.delete(task)
        db.session.flush()
