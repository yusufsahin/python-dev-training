from __future__ import annotations

from mongoengine import DateField, Document, StringField

TASK_STATUSES = ("todo", "in_progress", "done")


class Task(Document):
    """MongoEngine document — collection `task_item` (ch09 ile aynı mantıksal tablo adı)."""

    meta = {"collection": "task_item"}

    title = StringField(max_length=200, required=True)
    status = StringField(max_length=20, required=True, default="todo")
    start_date = DateField(required=False, null=True)
    end_date = DateField(required=False, null=True)

    def __repr__(self) -> str:
        return f"<Task {self.id} {self.title!r}>"
