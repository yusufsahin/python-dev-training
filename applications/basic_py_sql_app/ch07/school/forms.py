from __future__ import annotations

from typing import TYPE_CHECKING

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField
from wtforms.validators import DataRequired, Length

if TYPE_CHECKING:
    from school.models import Department


class DepartmentForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(max=100)],
        render_kw={
            "class": "form-control",
            "placeholder": "Department name",
            "autocomplete": "organization",
        },
    )


class StudentForm(FlaskForm):
    student_number = StringField(
        "Student number",
        validators=[DataRequired(), Length(max=20)],
        render_kw={
            "class": "form-control",
            "placeholder": "e.g. 2024001",
        },
    )
    first_name = StringField(
        "First name",
        validators=[DataRequired(), Length(max=50)],
        render_kw={"class": "form-control"},
    )
    last_name = StringField(
        "Last name",
        validators=[DataRequired(), Length(max=50)],
        render_kw={"class": "form-control"},
    )
    birth_date = DateField(
        "Birth date",
        validators=[DataRequired()],
        format="%Y-%m-%d",
        render_kw={"class": "form-control", "type": "date"},
    )
    department = SelectField(
        "Department",
        coerce=int,
        validators=[DataRequired()],
        render_kw={"class": "form-select"},
        choices=[],
    )

    def apply_department_choices(self, departments: list[Department]) -> None:
        self.department.choices = [(d.id, d.name) for d in departments]
