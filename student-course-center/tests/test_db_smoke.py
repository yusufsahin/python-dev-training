import os

import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get("STUDENT_COURSE_CENTER_CONNECTION_STRING", "").strip(),
    reason="STUDENT_COURSE_CENTER_CONNECTION_STRING not set",
)


def test_ping() -> None:
    from student_course_center.application import services

    rows = services.ping()
    assert rows and rows[0].get("Ok") == 1


def test_list_students() -> None:
    from student_course_center.application import services

    rows = services.list_students(institution_id=1)
    assert isinstance(rows, list)
