"""Task Create/Update/Response şemaları."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_validator


TaskStatus = Literal["todo", "in_progress", "done", "cancelled"]


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    priority: int = 2
    status: TaskStatus = "todo"
    due_date: str | None = None
    category_id: int | None = None

    @field_validator("title")
    @classmethod
    def title_min_length(cls, v: str) -> str:
        if not (v and v.strip()):
            raise ValueError("Başlık en az 1 karakter olmalı")
        return v.strip()

    @field_validator("priority")
    @classmethod
    def priority_range(cls, v: int) -> int:
        if v not in (1, 2, 3, 4):
            raise ValueError("Öncelik 1-4 arası olmalı")
        return v


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = None
    status: TaskStatus | None = None
    due_date: str | None = None
    category_id: int | None = None

    @field_validator("title")
    @classmethod
    def title_min_length(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Başlık en az 1 karakter olmalı")
        return v.strip() if v else None

    @field_validator("priority")
    @classmethod
    def priority_range(cls, v: int | None) -> int | None:
        if v is not None and v not in (1, 2, 3, 4):
            raise ValueError("Öncelik 1-4 arası olmalı")
        return v


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    status: str
    due_date: str | None
    category_id: int | None
    created_at: datetime
    updated_at: datetime
    category_name: str | None = None
    category_color: str | None = None

    model_config = {"from_attributes": True}
