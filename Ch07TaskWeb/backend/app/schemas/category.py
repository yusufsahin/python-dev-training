"""Category Create/Response şemaları."""
import re

from pydantic import BaseModel, field_validator


class CategoryCreate(BaseModel):
    name: str
    color: str = "#808080"

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not (v and v.strip()):
            raise ValueError("Kategori adı boş olamaz")
        return v.strip()

    @field_validator("color")
    @classmethod
    def color_hex(cls, v: str) -> str:
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Renk #RRGGBB formatında olmalı")
        return v


class CategoryResponse(BaseModel):
    id: int
    name: str
    color: str

    model_config = {"from_attributes": True}
