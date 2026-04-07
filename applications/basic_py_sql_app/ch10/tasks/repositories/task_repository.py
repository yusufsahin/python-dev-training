from __future__ import annotations

from bson import ObjectId
from bson.errors import InvalidId

from tasks.models import Task


class MongoTaskRepository:
    def _qs(self):
        return Task.objects

    def list_all(self) -> list[Task]:
        return list(self._qs().order_by("-id"))

    def get_by_id(self, task_id: str) -> Task | None:
        tid = (task_id or "").strip()
        if not tid:
            return None
        try:
            oid = ObjectId(tid)
        except InvalidId:
            return None
        doc = self._qs().filter(id=oid).first()
        return doc

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
        t.save()
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
        task.save()
        return task

    def delete(self, task: Task) -> None:
        task.delete()
