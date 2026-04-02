from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Department(Base):
    __tablename__ = "school_department"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="department",
        lazy="selectin",
    )


class Student(Base):
    __tablename__ = "school_student"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("school_department.id", ondelete="RESTRICT"),
        nullable=False,
    )

    department: Mapped[Department] = relationship("Department", back_populates="students")
