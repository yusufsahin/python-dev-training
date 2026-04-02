"""REST API (/api/...). JSON istek/gövde; servis katmanını doğrudan kullanır."""

import json
from datetime import date
from typing import Any
from urllib.parse import urlparse

from dependencies import department_service, student_service
from dto.department_dto import DepartmentRequest
from dto.student_dto import StudentRequest
from models.department import Department
from models.student import Student

from web.http_utils import db_error_message, parse_birth_date


def _json_default(obj: Any) -> str:
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _student_to_dict(s: Student) -> dict[str, Any]:
    return {
        "id": s.id,
        "student_number": s.student_number,
        "first_name": s.first_name,
        "last_name": s.last_name,
        "birth_date": s.birth_date.isoformat(),
        "department_name": s.department_name,
    }


def _department_to_dict(d: Department) -> dict[str, Any]:
    return {"id": d.id, "name": d.name}


def json_response(handler, data: Any, status: int = 200) -> None:
    body = json.dumps(data, default=_json_default).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def error_response(handler, message: str, status: int = 400) -> None:
    json_response(handler, {"error": message}, status)


def read_json_body(handler) -> dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    if length == 0:
        return {}
    raw = handler.rfile.read(length).decode("utf-8")
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON body.") from exc
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object.")
    return data


def _parse_student_request(data: dict[str, Any]) -> StudentRequest:
    try:
        sn = str(data["student_number"]).strip()
        fn = str(data["first_name"]).strip()
        ln = str(data["last_name"]).strip()
        dept_id = int(data["department_id"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(
            "Required fields: student_number, first_name, last_name, "
            "birth_date (YYYY-MM-DD), department_id (integer)."
        ) from exc

    if not sn or not fn or not ln:
        raise ValueError("student_number, first_name and last_name cannot be empty.")

    bd_raw = data.get("birth_date")
    if bd_raw is None:
        raise ValueError("birth_date is required (YYYY-MM-DD).")
    if isinstance(bd_raw, str):
        try:
            birth_date = parse_birth_date(bd_raw)
        except ValueError as exc:
            raise ValueError("birth_date must be YYYY-MM-DD.") from exc
    else:
        raise ValueError("birth_date must be a string (YYYY-MM-DD).")

    if not department_service.is_valid_department(dept_id):
        raise ValueError("Invalid department_id.")

    return StudentRequest(
        student_number=sn,
        first_name=fn,
        last_name=ln,
        birth_date=birth_date,
        department_id=dept_id,
    )


def _parse_department_body(data: dict[str, Any]) -> str:
    name = data.get("name")
    if name is None or not str(name).strip():
        raise ValueError("Field 'name' is required and cannot be empty.")
    return str(name).strip()


def _api_segments(path: str) -> list[str]:
    """'/api/students/3' -> ['students', '3']"""
    p = path.rstrip("/")
    if not p.startswith("/api"):
        return []
    rest = p.removeprefix("/api").strip("/")
    if not rest:
        return []
    return rest.split("/")


def handle_api_options(handler) -> None:
    handler.send_response(204)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header(
        "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
    )
    handler.send_header(
        "Access-Control-Allow-Headers", "Content-Type, Authorization"
    )
    handler.send_header("Access-Control-Max-Age", "86400")
    handler.end_headers()


def handle_api_get(handler) -> None:
    path = urlparse(handler.path).path.rstrip("/") or "/"
    segs = _api_segments(path)

    try:
        if path == "/api" or not segs:
            json_response(
                handler,
                {
                    "name": "student-app-api",
                    "endpoints": {
                        "GET /api/health": "Health check",
                        "GET /api/departments": "List departments",
                        "GET /api/departments/{id}": "Get department",
                        "POST /api/departments": "Create department body: {name}",
                        "PUT /api/departments/{id}": "Update department body: {name}",
                        "DELETE /api/departments/{id}": "Delete department",
                        "GET /api/students": "List students",
                        "GET /api/students/{id}": "Get student",
                        "POST /api/students": "Create student (JSON body)",
                        "PUT /api/students/{id}": "Update student (JSON body)",
                        "DELETE /api/students/{id}": "Delete student",
                        "POST /api/setup/init": "Create database schema",
                        "POST /api/setup/seed": "Load demo seed data",
                    },
                },
            )
            return

        if segs == ["departments"]:
            items = department_service.get_departments()
            json_response(handler, {"items": [_department_to_dict(d) for d in items]})
            return
        if len(segs) == 2 and segs[0] == "departments":
            did = int(segs[1])
            d = department_service.get_department(did)
            if d is None:
                error_response(handler, "Department not found.", 404)
                return
            json_response(handler, _department_to_dict(d))
            return

        if segs == ["students"]:
            items = student_service.get_students()
            json_response(handler, {"items": [_student_to_dict(s) for s in items]})
            return
        if len(segs) == 2 and segs[0] == "students":
            sid = int(segs[1])
            s = student_service.get_student(sid)
            if s is None:
                error_response(handler, "Student not found.", 404)
                return
            json_response(handler, _student_to_dict(s))
            return

        if segs == ["health"]:
            json_response(handler, {"status": "ok"})
            return

        error_response(handler, "Not found.", 404)
    except ValueError:
        error_response(handler, "Invalid resource id.", 400)
    except Exception as exc:
        error_response(handler, db_error_message(exc), 503)


def handle_api_post(handler) -> None:
    path = urlparse(handler.path).path
    segs = _api_segments(path)

    try:
        data = read_json_body(handler)
    except ValueError as exc:
        error_response(handler, str(exc), 400)
        return

    try:
        if segs == ["setup", "init"]:
            student_service.initialize_app()
            json_response(handler, {"ok": True, "message": "Schema ready."}, 201)
            return
        if segs == ["setup", "seed"]:
            n = student_service.load_seed_data()
            json_response(
                handler, {"ok": True, "students_inserted": n, "message": f"Seed done ({n} rows)."}, 201
            )
            return

        if segs == ["departments"]:
            name = _parse_department_body(data)
            ok = department_service.add_department(DepartmentRequest(name=name))
            if not ok:
                error_response(handler, "Department name already exists.", 409)
                return
            json_response(handler, {"ok": True, "message": "Department created."}, 201)
            return

        if segs == ["students"]:
            req = _parse_student_request(data)
            ok = student_service.add_student(req)
            if not ok:
                error_response(handler, "Student number already exists.", 409)
                return
            json_response(handler, {"ok": True, "message": "Student created."}, 201)
            return

        error_response(handler, "Not found.", 404)
    except ValueError as exc:
        error_response(handler, str(exc), 400)
    except Exception as exc:
        error_response(handler, db_error_message(exc), 503)


def handle_api_put(handler) -> None:
    path = urlparse(handler.path).path
    segs = _api_segments(path)

    try:
        data = read_json_body(handler)
    except ValueError as exc:
        error_response(handler, str(exc), 400)
        return

    try:
        if len(segs) == 2 and segs[0] == "departments":
            did = int(segs[1])
            name = _parse_department_body(data)
            result = department_service.edit_department(did, DepartmentRequest(name=name))
            if result == "not_found":
                error_response(handler, "Department not found.", 404)
                return
            if result == "conflict":
                error_response(handler, "Department name already exists.", 409)
                return
            json_response(handler, {"ok": True, "message": "Department updated."})
            return

        if len(segs) == 2 and segs[0] == "students":
            sid = int(segs[1])
            req = _parse_student_request(data)
            ok = student_service.edit_student(sid, req)
            if not ok:
                error_response(handler, "Student not found.", 404)
                return
            json_response(handler, {"ok": True, "message": "Student updated."})
            return

        error_response(handler, "Not found.", 404)
    except ValueError as exc:
        error_response(handler, str(exc), 400)
    except Exception as exc:
        error_response(handler, db_error_message(exc), 503)


def handle_api_delete(handler) -> None:
    path = urlparse(handler.path).path
    segs = _api_segments(path)

    try:
        if len(segs) == 2 and segs[0] == "departments":
            did = int(segs[1])
            result = department_service.remove_department(did)
            if result == "not_found":
                error_response(handler, "Department not found.", 404)
                return
            if result == "in_use":
                error_response(handler, "Department is in use by students.", 409)
                return
            json_response(handler, {"ok": True, "message": "Department deleted."})
            return

        if len(segs) == 2 and segs[0] == "students":
            sid = int(segs[1])
            ok = student_service.remove_student(sid)
            if not ok:
                error_response(handler, "Student not found.", 404)
                return
            json_response(handler, {"ok": True, "message": "Student deleted."})
            return

        error_response(handler, "Not found.", 404)
    except ValueError:
        error_response(handler, "Invalid resource id.", 400)
    except Exception as exc:
        error_response(handler, db_error_message(exc), 503)


def is_api_path(path: str) -> bool:
    return path == "/api" or path.startswith("/api/")


def dispatch_api(handler, method: str) -> bool:
    """True if istek API tarafından işlendi."""
    path = urlparse(handler.path).path
    if not is_api_path(path):
        return False

    if method == "OPTIONS":
        handle_api_options(handler)
        return True
    if method == "GET":
        handle_api_get(handler)
        return True
    if method == "POST":
        handle_api_post(handler)
        return True
    if method == "PUT":
        handle_api_put(handler)
        return True
    if method == "DELETE":
        handle_api_delete(handler)
        return True

    handler.send_response(405)
    handler.send_header("Allow", "GET, POST, PUT, DELETE, OPTIONS")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    return True
