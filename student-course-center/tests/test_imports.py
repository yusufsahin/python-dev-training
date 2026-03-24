"""No database required."""

import pytest

from student_course_center.console.main import main


def test_package_version() -> None:
    import student_course_center

    assert student_course_center.__version__


def test_main_help_system_exit_zero() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_list_students_help_system_exit_zero() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["list", "students", "--help"])
    assert exc.value.code == 0


def test_seed_faker_dry_run_returns_zero() -> None:
    assert main(["seed", "faker", "--dry-run"]) == 0
