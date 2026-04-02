"""REST API (JSON) — Pydantic doğrulama, mevcut servis katmanı."""

from __future__ import annotations

from typing import Any

from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError as PydanticValidationError

from school.exceptions import ValidationError as AppValidationError
from school.extensions import csrf
from school.schemas.api import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentUpdate,
    StudentCreate,
    StudentRead,
    StudentUpdate,
)
from school.services import DepartmentService, StudentService

bp = Blueprint("api", __name__)


def _json_error(
    message: str | None = None,
    *,
    errors: list[str] | None = None,
    status: int = 400,
) -> tuple[Response, int]:
    body: dict[str, Any] = {}
    if message:
        body["detail"] = message
    if errors:
        body["errors"] = errors
    return jsonify(body), status


def _parse_json() -> Any | None:
    if not request.is_json:
        return None
    return request.get_json(silent=True)


@bp.get("/")
@csrf.exempt
def api_index() -> tuple[Response, int]:
    return (
        jsonify(
            {
                "name": "school-api",
                "version": 1,
                "endpoints": {
                    "health": "/api/v1/health",
                    "departments": "/api/v1/departments",
                    "students": "/api/v1/students",
                },
            }
        ),
        200,
    )


@bp.get("/health")
@csrf.exempt
def health() -> tuple[Response, int]:
    return jsonify({"status": "ok"}), 200


# --- Departments ---


@bp.get("/departments")
@csrf.exempt
def list_departments() -> tuple[Response, int]:
    rows = DepartmentService().list_departments()
    data = [DepartmentRead.model_validate(d).model_dump(mode="json") for d in rows]
    return jsonify(data), 200


@bp.post("/departments")
@csrf.exempt
def create_department() -> tuple[Response, int]:
    raw = _parse_json()
    if raw is None:
        return _json_error("Request body must be JSON", status=400)
    try:
        payload = DepartmentCreate.model_validate(raw)
    except PydanticValidationError as exc:
        return jsonify({"errors": exc.errors()}), 422
    try:
        d = DepartmentService().create_department(payload.name)
    except AppValidationError as exc:
        return _json_error(errors=exc.messages, status=400)
    out = DepartmentRead.model_validate(d).model_dump(mode="json")
    return jsonify(out), 201


@bp.get("/departments/<int:department_id>")
@csrf.exempt
def get_department(department_id: int) -> tuple[Response, int]:
    d = DepartmentService().get_department(department_id)
    if d is None:
        return _json_error("Department not found", status=404)
    return jsonify(DepartmentRead.model_validate(d).model_dump(mode="json")), 200


@bp.put("/departments/<int:department_id>")
@csrf.exempt
def update_department(department_id: int) -> tuple[Response, int]:
    raw = _parse_json()
    if raw is None:
        return _json_error("Request body must be JSON", status=400)
    try:
        payload = DepartmentUpdate.model_validate(raw)
    except PydanticValidationError as exc:
        return jsonify({"errors": exc.errors()}), 422
    try:
        d = DepartmentService().update_department(department_id, payload.name)
    except AppValidationError as exc:
        return _json_error(errors=exc.messages, status=400)
    return jsonify(DepartmentRead.model_validate(d).model_dump(mode="json")), 200


@bp.delete("/departments/<int:department_id>")
@csrf.exempt
def delete_department(department_id: int) -> tuple[Response, int]:
    try:
        DepartmentService().delete_department(department_id)
    except AppValidationError as exc:
        return _json_error(errors=exc.messages, status=400)
    return Response(status=204)


# --- Students ---


@bp.get("/students")
@csrf.exempt
def list_students() -> tuple[Response, int]:
    rows = StudentService().list_students()
    data = [StudentRead.model_validate(s).model_dump(mode="json") for s in rows]
    return jsonify(data), 200


@bp.post("/students")
@csrf.exempt
def create_student() -> tuple[Response, int]:
    raw = _parse_json()
    if raw is None:
        return _json_error("Request body must be JSON", status=400)
    try:
        payload = StudentCreate.model_validate(raw)
    except PydanticValidationError as exc:
        return jsonify({"errors": exc.errors()}), 422
    try:
        s = StudentService().create_student(
            student_number=payload.student_number,
            first_name=payload.first_name,
            last_name=payload.last_name,
            birth_date=payload.birth_date,
            department_id=payload.department_id,
        )
    except AppValidationError as exc:
        return _json_error(errors=exc.messages, status=400)
    out = StudentRead.model_validate(s).model_dump(mode="json")
    return jsonify(out), 201


@bp.get("/students/<int:student_id>")
@csrf.exempt
def get_student(student_id: int) -> tuple[Response, int]:
    s = StudentService().get_student(student_id)
    if s is None:
        return _json_error("Student not found", status=404)
    return jsonify(StudentRead.model_validate(s).model_dump(mode="json")), 200


@bp.put("/students/<int:student_id>")
@csrf.exempt
def update_student(student_id: int) -> tuple[Response, int]:
    raw = _parse_json()
    if raw is None:
        return _json_error("Request body must be JSON", status=400)
    try:
        payload = StudentUpdate.model_validate(raw)
    except PydanticValidationError as exc:
        return jsonify({"errors": exc.errors()}), 422
    try:
        s = StudentService().update_student(
            student_id,
            student_number=payload.student_number,
            first_name=payload.first_name,
            last_name=payload.last_name,
            birth_date=payload.birth_date,
            department_id=payload.department_id,
        )
    except AppValidationError as exc:
        return _json_error(errors=exc.messages, status=400)
    return jsonify(StudentRead.model_validate(s).model_dump(mode="json")), 200


@bp.delete("/students/<int:student_id>")
@csrf.exempt
def delete_student(student_id: int) -> tuple[Response, int]:
    try:
        StudentService().delete_student(student_id)
    except AppValidationError as exc:
        return _json_error(errors=exc.messages, status=400)
    return Response(status=204)
