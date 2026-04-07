from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


def _normalize_date(v: date | datetime | None) -> date | None:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.date()
    return v


class TaskReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    status: str
    start_date: date | None = None
    end_date: date | None = None

    @classmethod
    def from_mongo(cls, doc: dict) -> TaskReadDTO:
        return cls(
            id=str(doc["_id"]),
            title=doc["title"],
            status=doc["status"],
            start_date=_normalize_date(doc.get("start_date")),
            end_date=_normalize_date(doc.get("end_date")),
        )


class TaskCreateDTO(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: str
    start_date: date | None = None
    end_date: date | None = None


class TaskUpdateDTO(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    status: str
    start_date: date | None = None
    end_date: date | None = None
