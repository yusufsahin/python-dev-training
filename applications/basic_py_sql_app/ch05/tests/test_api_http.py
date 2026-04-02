import urllib.error
import urllib.request
from datetime import date

from models.department import Department
from models.student import Student

from tests.http_helpers import http_json


def test_api_health(api_server):
    base, _, _ = api_server
    status, data = http_json("GET", f"{base}/api/health")
    assert status == 200
    assert data["status"] == "ok"


def test_api_root_lists_endpoints(api_server):
    base, _, _ = api_server
    status, data = http_json("GET", f"{base}/api")
    assert status == 200
    assert "endpoints" in data
    assert "GET /api/students" in data["endpoints"]


def test_api_list_departments(api_server):
    base, _, md = api_server
    md.get_departments.return_value = [Department(1, "CS")]
    status, data = http_json("GET", f"{base}/api/departments")
    assert status == 200
    assert data["items"] == [{"id": 1, "name": "CS"}]
    md.get_departments.assert_called_once()


def test_api_get_department_not_found(api_server):
    base, _, md = api_server
    md.get_department.return_value = None
    status, data = http_json("GET", f"{base}/api/departments/99")
    assert status == 404
    assert "error" in data


def test_api_list_students(api_server):
    base, ms, _ = api_server
    ms.get_students.return_value = [
        Student(1, "N1", "A", "B", date(2000, 1, 1), "Dept"),
    ]
    status, data = http_json("GET", f"{base}/api/students")
    assert status == 200
    assert len(data["items"]) == 1
    assert data["items"][0]["student_number"] == "N1"
    assert data["items"][0]["birth_date"] == "2000-01-01"


def test_api_post_department_created(api_server):
    base, _, md = api_server
    md.add_department.return_value = True
    status, data = http_json("POST", f"{base}/api/departments", {"name": "Law"})
    assert status == 201
    assert data["ok"] is True


def test_api_post_department_conflict(api_server):
    base, _, md = api_server
    md.add_department.return_value = False
    status, data = http_json("POST", f"{base}/api/departments", {"name": "Dup"})
    assert status == 409


def test_api_post_student_validation(api_server):
    base, ms, md = api_server
    md.is_valid_department.return_value = True
    ms.add_student.return_value = True
    body = {
        "student_number": "T1",
        "first_name": "F",
        "last_name": "L",
        "birth_date": "1999-05-05",
        "department_id": 1,
    }
    status, data = http_json("POST", f"{base}/api/students", body)
    assert status == 201
    ms.add_student.assert_called_once()
    req = ms.add_student.call_args[0][0]
    assert req.student_number == "T1"


def test_api_post_student_invalid_department(api_server):
    base, _, md = api_server
    md.is_valid_department.return_value = False
    body = {
        "student_number": "T1",
        "first_name": "F",
        "last_name": "L",
        "birth_date": "1999-05-05",
        "department_id": 999,
    }
    status, data = http_json("POST", f"{base}/api/students", body)
    assert status == 400
    assert "department" in data["error"].lower()


def test_api_put_department(api_server):
    base, _, md = api_server
    md.edit_department.return_value = "updated"
    status, data = http_json("PUT", f"{base}/api/departments/3", {"name": "Bio"})
    assert status == 200
    md.edit_department.assert_called_once()


def test_api_delete_student_not_found(api_server):
    base, ms, _ = api_server
    ms.remove_student.return_value = False
    status, data = http_json("DELETE", f"{base}/api/students/404")
    assert status == 404


def test_api_options_cors(api_server):
    base, _, _ = api_server
    req = urllib.request.Request(
        f"{base}/api/students", method="OPTIONS", headers={"Origin": "http://x"}
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        assert resp.status == 204
        assert resp.headers.get("Access-Control-Allow-Origin") == "*"


def test_api_invalid_json(api_server):
    base, _, _ = api_server
    req = urllib.request.Request(
        f"{base}/api/departments",
        data=b"{not json",
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
        assert False, "expected HTTPError"
    except urllib.error.HTTPError as e:
        assert e.code == 400
