from __future__ import annotations

from datetime import date, datetime, time, timezone

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorCollection


def parse_object_id(task_id: str) -> ObjectId | None:
    tid = (task_id or "").strip()
    if not tid or not ObjectId.is_valid(tid):
        return None
    try:
        return ObjectId(tid)
    except InvalidId:
        return None


def dates_to_bson(start: date | None, end: date | None) -> tuple[datetime | None, datetime | None]:
    def one(d: date | None) -> datetime | None:
        if d is None:
            return None
        return datetime.combine(d, time.min, tzinfo=timezone.utc)

    return one(start), one(end)


class TaskRepository:
    async def list_all(self, coll: AsyncIOMotorCollection) -> list[dict]:
        cursor = coll.find().sort("_id", -1)
        return await cursor.to_list(length=5000)

    async def get_by_oid(self, coll: AsyncIOMotorCollection, oid: ObjectId) -> dict | None:
        return await coll.find_one({"_id": oid})

    async def insert(
        self,
        coll: AsyncIOMotorCollection,
        *,
        title: str,
        status: str,
        start_date: date | None,
        end_date: date | None,
    ) -> dict:
        sd, ed = dates_to_bson(start_date, end_date)
        doc = {
            "title": title,
            "status": status,
            "start_date": sd,
            "end_date": ed,
        }
        res = await coll.insert_one(doc)
        out = await coll.find_one({"_id": res.inserted_id})
        assert out is not None
        return out

    async def update(
        self,
        coll: AsyncIOMotorCollection,
        oid: ObjectId,
        *,
        title: str,
        status: str,
        start_date: date | None,
        end_date: date | None,
    ) -> dict | None:
        sd, ed = dates_to_bson(start_date, end_date)
        result = await coll.update_one(
            {"_id": oid},
            {"$set": {
                "title": title,
                "status": status,
                "start_date": sd,
                "end_date": ed,
            }},
        )
        if result.matched_count == 0:
            return None
        return await coll.find_one({"_id": oid})

    async def delete(self, coll: AsyncIOMotorCollection, oid: ObjectId) -> bool:
        res = await coll.delete_one({"_id": oid})
        return res.deleted_count > 0
