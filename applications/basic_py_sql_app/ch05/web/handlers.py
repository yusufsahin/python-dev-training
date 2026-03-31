from datetime import datetime
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from controllers.department_controller import (
    handle_add_department,
    handle_delete_department,
    handle_get_department,
    handle_initialize_app,
    handle_is_valid_department,
    handle_list_departments,
    handle_seed_data,
    handle_update_department,
)
from controllers.student_controller import (
    handle_add_student,
    handle_delete_student,
    handle_get_student,
    handle_list_students,
    handle_update_student,
)
from dto.department_dto import DepartmentRequest
from dto.student_dto import StudentRequest
from web.views import (
    dashboard_page,
    department_detail_page,
    departments_page,
    redirect_url,
    student_detail_page,
    students_page,
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


def parse_birth_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def read_form_data(handler) -> dict[str, str]:
    content_length = int(handler.headers.get("Content-Length", "0"))
    raw_body = handler.rfile.read(content_length).decode("utf-8")
    parsed = parse_qs(raw_body)
    return {key: values[0].strip() for key, values in parsed.items()}


def read_message(path: str) -> str:
    query = parse_qs(urlparse(path).query)
    return query.get("message", [""])[0]


def parse_int(value: str, field_name: str) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must be a number.") from error


def safe_students() -> tuple[list, str]:
    try:
        return handle_list_students(), ""
    except Exception:
        return [], "Database is not ready yet. Use Create Tables first."


def safe_departments() -> tuple[list, str]:
    try:
        return handle_list_departments(), ""
    except Exception:
        return [], "Database is not ready yet. Use Create Tables first."


def safe_student(student_id: int):
    try:
        return handle_get_student(student_id), ""
    except Exception:
        return None, "Database is not ready yet. Use Create Tables first."


def safe_department(department_id: int):
    try:
        return handle_get_department(department_id), ""
    except Exception:
        return None, "Database is not ready yet. Use Create Tables first."


def build_student_request(form_data: dict[str, str]) -> StudentRequest:
    student_number = form_data.get("student_number", "")
    first_name = form_data.get("first_name", "")
    last_name = form_data.get("last_name", "")
    birth_date_text = form_data.get("birth_date", "")
    department_value = form_data.get("department_id", "")

    if not student_number:
        raise ValueError("Student number cannot be empty.")
    if not first_name or not last_name:
        raise ValueError("First name and last name cannot be empty.")

    try:
        birth_date = parse_birth_date(birth_date_text)
    except ValueError as error:
        raise ValueError("Invalid birth date format. Use YYYY-MM-DD.") from error

    department_id = parse_int(department_value, "Department ID")
    try:
        is_valid_department = handle_is_valid_department(department_id)
    except Exception as error:
        raise ValueError("Database is not ready yet. Use Create Tables first.") from error

    if not is_valid_department:
        raise ValueError("Invalid department ID.")

    return StudentRequest(
        student_number=student_number,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        department_id=department_id,
    )


def serve_static(handler, path: str) -> bool:
    relative_path = path.removeprefix("/static/")
    file_path = STATIC_DIR / relative_path

    if not file_path.exists() or not file_path.is_file():
        return False

    content_type = "text/plain; charset=utf-8"
    if file_path.suffix == ".css":
        content_type = "text/css; charset=utf-8"
    if file_path.suffix == ".js":
        content_type = "application/javascript; charset=utf-8"

    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.end_headers()
    handler.wfile.write(file_path.read_bytes())
    return True


def html_response(handler, html: str, status_code: int = 200) -> None:
    body = html.encode("utf-8")
    handler.send_response(status_code)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def redirect(handler, location: str) -> None:
    handler.send_response(303)
    handler.send_header("Location", location)
    handler.end_headers()


def handle_get_request(handler) -> None:
    parsed_url = urlparse(handler.path)
    path = parsed_url.path
    message = read_message(handler.path)

    if path.startswith("/static/"):
        if serve_static(handler, path):
            return
        html_response(handler, "<h1>Static file not found</h1>", 404)
        return

    if path == "/":
        students, students_error = safe_students()
        departments, departments_error = safe_departments()
        html_response(
            handler,
            dashboard_page(
                len(students),
                len(departments),
                message or students_error or departments_error,
            ),
        )
        return

    if path == "/students":
        students, students_error = safe_students()
        departments, departments_error = safe_departments()
        html_response(
            handler,
            students_page(
                students,
                departments,
                message or students_error or departments_error,
            ),
        )
        return

    if path == "/departments":
        departments, departments_error = safe_departments()
        html_response(handler, departments_page(departments, message or departments_error))
        return

    if path.startswith("/students/"):
        student_id = path.split("/")[-1]
        try:
            student, student_error = safe_student(parse_int(student_id, "Student ID"))
        except ValueError:
            html_response(handler, student_detail_page(None, "Invalid student ID."), 400)
            return

        html_response(handler, student_detail_page(student, message or student_error))
        return

    if path.startswith("/departments/"):
        department_id = path.split("/")[-1]
        try:
            department, department_error = safe_department(
                parse_int(department_id, "Department ID")
            )
        except ValueError:
            html_response(
                handler, department_detail_page(None, "Invalid department ID."), 400
            )
            return

        html_response(
            handler, department_detail_page(department, message or department_error)
        )
        return

    html_response(handler, "<h1>Page not found</h1>", 404)


def handle_post_request(handler) -> None:
    path = urlparse(handler.path).path
    form_data = read_form_data(handler)

    try:
        if path == "/setup/init":
            redirect(handler, redirect_url("/", handle_initialize_app()))
            return

        if path == "/setup/seed":
            redirect(handler, redirect_url("/", handle_seed_data()))
            return

        if path == "/departments/create":
            name = form_data.get("name", "")
            if not name:
                raise ValueError("Department name cannot be empty.")

            message = handle_add_department(DepartmentRequest(name=name))
            redirect(handler, redirect_url("/departments", message))
            return

        if path == "/departments/update":
            department_id = parse_int(form_data.get("department_id", ""), "Department ID")
            name = form_data.get("name", "")
            if not name:
                raise ValueError("Department name cannot be empty.")

            message = handle_update_department(department_id, DepartmentRequest(name=name))
            redirect(handler, redirect_url("/departments", message))
            return

        if path == "/departments/delete":
            department_id = parse_int(form_data.get("department_id", ""), "Department ID")
            redirect(
                handler,
                redirect_url("/departments", handle_delete_department(department_id)),
            )
            return

        if path == "/students/create":
            student_request = build_student_request(form_data)
            redirect(handler, redirect_url("/students", handle_add_student(student_request)))
            return

        if path == "/students/update":
            student_id = parse_int(form_data.get("student_id", ""), "Student ID")
            student_request = build_student_request(form_data)
            redirect(
                handler,
                redirect_url("/students", handle_update_student(student_id, student_request)),
            )
            return

        if path == "/students/delete":
            student_id = parse_int(form_data.get("student_id", ""), "Student ID")
            redirect(handler, redirect_url("/students", handle_delete_student(student_id)))
            return

        redirect(handler, redirect_url("/", "Unknown action."))
    except ValueError as error:
        target = "/students" if path.startswith("/students") else "/departments"
        if path.startswith("/setup"):
            target = "/"
        redirect(handler, redirect_url(target, str(error)))
    except Exception:
        target = "/students" if path.startswith("/students") else "/departments"
        if path.startswith("/setup"):
            target = "/"
        redirect(handler, redirect_url(target, "Database is not ready yet. Use Create Tables first."))


class StudentAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        handle_get_request(self)

    def do_POST(self):
        handle_post_request(self)

    def log_message(self, format, *args):
        return
