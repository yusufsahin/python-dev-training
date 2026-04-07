"""Initial demo tasks when the collection is empty."""

from __future__ import annotations

from datetime import date, datetime, timedelta, time, timezone

from motor.motor_asyncio import AsyncIOMotorCollection


def _dt(d: date) -> datetime:
    return datetime.combine(d, time.min, tzinfo=timezone.utc)


async def ensure_initial_data(coll: AsyncIOMotorCollection) -> None:
    if await coll.count_documents({}) > 0:
        return
    today = date.today()
    samples = [
        ("Plan sprint", "todo", today, today + timedelta(days=7)),
        ("Review pull requests", "in_progress", today - timedelta(days=1), today + timedelta(days=2)),
        ("Deploy hotfix", "done", today - timedelta(days=5), today - timedelta(days=4)),
    ]
    for title, status, start, end in samples:
        await coll.insert_one({
            "title": title,
            "status": status,
            "start_date": _dt(start),
            "end_date": _dt(end),
        })
