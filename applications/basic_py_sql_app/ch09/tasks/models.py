from __future__ import annotations

from tasks.extensions import db

TASK_STATUSES = ("todo", "in_progress", "done")


class Task(db.Model):
    __tablename__ = "task_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="todo")
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    def __repr__(self) -> str:
        return f"<Task {self.id} {self.title!r}>"
