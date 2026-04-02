from __future__ import annotations

from school.extensions import db


class Department(db.Model):
    __tablename__ = "school_department"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    students = db.relationship(
        "Student",
        back_populates="department",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return self.name


class Student(db.Model):
    __tablename__ = "school_student"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    department_id = db.Column(
        db.Integer,
        db.ForeignKey("school_department.id", ondelete="RESTRICT"),
        nullable=False,
    )

    department = db.relationship("Department", back_populates="students")

    def __repr__(self) -> str:
        return f"{self.student_number} ({self.first_name} {self.last_name})"
