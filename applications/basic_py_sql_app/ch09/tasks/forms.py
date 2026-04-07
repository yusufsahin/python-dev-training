from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Optional

def _status_choices() -> list[tuple[str, str]]:
    return [
        ("todo", "Todo"),
        ("in_progress", "In progress"),
        ("done", "Done"),
    ]


class TaskForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)],
        render_kw={
            "class": "form-control",
            "placeholder": "Task title",
            "autocomplete": "off",
        },
    )
    status = SelectField(
        "Status",
        coerce=str,
        choices=[],
        validators=[DataRequired()],
        render_kw={"class": "form-select"},
    )
    start_date = DateField(
        "Start date",
        validators=[Optional()],
        format="%Y-%m-%d",
        render_kw={"class": "form-control", "type": "date"},
    )
    end_date = DateField(
        "End date",
        validators=[Optional()],
        format="%Y-%m-%d",
        render_kw={"class": "form-control", "type": "date"},
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.status.choices = _status_choices()
