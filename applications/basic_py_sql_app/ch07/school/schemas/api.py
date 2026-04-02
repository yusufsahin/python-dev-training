"""Pydantic v2 şemaları — REST istek/gövde ve ORM yanıtları."""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DepartmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class DepartmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class DepartmentUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_number: str
    first_name: str
    last_name: str
    birth_date: date
    department_id: int
    department: DepartmentRead


class StudentCreate(BaseModel):
    student_number: str = Field(min_length=1, max_length=20)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    birth_date: date
    department_id: int = Field(gt=0)

    @field_validator("student_number", "first_name", "last_name")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()


class StudentUpdate(BaseModel):
    student_number: str = Field(min_length=1, max_length=20)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    birth_date: date
    department_id: int = Field(gt=0)

    @field_validator("student_number", "first_name", "last_name")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()


class ErrorResponse(BaseModel):
    detail: str | None = None
    errors: list[str] | None = None
