"""Demo tasks (MongoDB)."""

from __future__ import annotations

from datetime import date, timedelta

from tasks.models import Task


def seed_demo_data() -> None:
    today = date.today()
    samples = [
        ("Plan sprint", "todo", today, today + timedelta(days=7)),
        ("Review pull requests", "in_progress", today - timedelta(days=1), today + timedelta(days=2)),
        ("Deploy hotfix", "done", today - timedelta(days=5), today - timedelta(days=4)),
    ]
    for title, status, start, end in samples:
        Task(
            title=title,
            status=status,
            start_date=start,
            end_date=end,
        ).save()
    print(f"Seeded {len(samples)} tasks.")
