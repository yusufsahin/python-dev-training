from html import escape
from pathlib import Path
from urllib.parse import quote_plus

TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def load_template(name: str) -> str:
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def render_template(name: str, context: dict[str, object]) -> str:
    content = load_template(name)
    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))
    return content


def render_partial(name: str, context: dict[str, object] | None = None) -> str:
    return render_template(f"partials/{name}", context or {})


def render_flash_message(message: str) -> str:
    if not message:
        return ""
    return render_partial("flash.html", {"message": escape(message)})


def page_layout(title: str, content: str, message: str = "") -> str:
    return render_template(
        "layout.html",
        {
            "title": escape(title),
            "site_header": render_partial("site_header.html"),
            "flash_message": render_flash_message(message),
            "content": content,
        },
    )


def dashboard_page(student_count: int, department_count: int, message: str = "") -> str:
    content = render_template(
        "dashboard.html",
        {
            "student_count": student_count,
            "department_count": department_count,
        },
    )
    return page_layout("Home", content, message)


def department_options(departments: list, selected_id: int | None = None) -> str:
    options = []
    for department in departments:
        selected = " selected" if department.id == selected_id else ""
        options.append(
            f'<option value="{department.id}"{selected}>{escape(department.name)}</option>'
        )
    return "".join(options)


def student_rows(students: list) -> str:
    rows = []
    for student in students:
        rows.append(
            f"""
            <tr>
                <td>{student.id}</td>
                <td><a href="/students/{student.id}">{escape(student.student_number)}</a></td>
                <td>{escape(student.first_name)} {escape(student.last_name)}</td>
                <td>{student.birth_date}</td>
                <td>{escape(student.department_name)}</td>
                <td>
                    <form method="post" action="/students/delete" class="inline-form danger-form">
                        <input type="hidden" name="student_id" value="{student.id}">
                        <button type="submit">Delete</button>
                    </form>
                </td>
            </tr>
            """
        )

    if not rows:
        rows.append('<tr><td colspan="6">No students found.</td></tr>')

    return "".join(rows)


def students_page(students: list, departments: list, message: str = "") -> str:
    content = render_template(
        "students.html",
        {
            "department_options": department_options(departments),
            "student_rows": student_rows(students),
        },
    )
    return page_layout("Students", content, message)


def department_rows(departments: list) -> str:
    rows = []
    for department in departments:
        rows.append(
            f"""
            <tr>
                <td>{department.id}</td>
                <td><a href="/departments/{department.id}">{escape(department.name)}</a></td>
                <td>
                    <form method="post" action="/departments/delete" class="inline-form danger-form">
                        <input type="hidden" name="department_id" value="{department.id}">
                        <button type="submit">Delete</button>
                    </form>
                </td>
            </tr>
            """
        )

    if not rows:
        rows.append('<tr><td colspan="3">No departments found.</td></tr>')

    return "".join(rows)


def departments_page(departments: list, message: str = "") -> str:
    content = render_template(
        "departments.html",
        {
            "department_rows": department_rows(departments),
        },
    )
    return page_layout("Departments", content, message)


def student_detail_page(student, message: str = "") -> str:
    if student is None:
        body = "<p>Student not found.</p>"
        content = render_template(
            "student_detail.html",
            {"heading": "Student Detail", "body": body},
        )
        return page_layout("Student Detail", content, message)

    body = f"""
    <dl>
        <dt>ID</dt><dd>{student.id}</dd>
        <dt>Student Number</dt><dd>{escape(student.student_number)}</dd>
        <dt>First Name</dt><dd>{escape(student.first_name)}</dd>
        <dt>Last Name</dt><dd>{escape(student.last_name)}</dd>
        <dt>Birth Date</dt><dd>{student.birth_date}</dd>
        <dt>Department</dt><dd>{escape(student.department_name)}</dd>
    </dl>
    """
    content = render_template(
        "student_detail.html",
        {"heading": "Student Detail", "body": body},
    )
    return page_layout("Student Detail", content, message)


def department_detail_page(department, message: str = "") -> str:
    if department is None:
        body = "<p>Department not found.</p>"
        content = render_template(
            "department_detail.html",
            {"heading": "Department Detail", "body": body},
        )
        return page_layout("Department Detail", content, message)

    body = f"""
    <dl>
        <dt>ID</dt><dd>{department.id}</dd>
        <dt>Name</dt><dd>{escape(department.name)}</dd>
    </dl>
    """
    content = render_template(
        "department_detail.html",
        {"heading": "Department Detail", "body": body},
    )
    return page_layout("Department Detail", content, message)


def redirect_url(path: str, message: str = "") -> str:
    if not message:
        return path
    return f"{path}?message={quote_plus(message)}"
