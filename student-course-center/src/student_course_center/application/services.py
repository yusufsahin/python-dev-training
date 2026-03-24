from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from student_course_center.infrastructure import db


def ping() -> list[dict[str, Any]]:
    columns, rows = db.fetch_all("SELECT 1 AS Ok")
    return db.rows_as_dicts(columns, rows)


def list_students(
    institution_id: int | None = None,
    active_only: bool = True,
) -> list[dict[str, Any]]:
    base = """
        SELECT StudentId, InstitutionId, StudentNo, FirstName, LastName,
               GradeLevel, SchoolName, Phone, Email, IsActive
        FROM dbo.Students
    """
    clauses: list[str] = []
    params: list[Any] = []
    if institution_id is not None:
        clauses.append("InstitutionId = ?")
        params.append(institution_id)
    if active_only:
        clauses.append("IsActive = 1")
    if clauses:
        base += " WHERE " + " AND ".join(clauses)
    base += " ORDER BY StudentId"
    columns, rows = db.fetch_all(base, tuple(params))
    return db.rows_as_dicts(columns, rows)


def list_teachers(
    institution_id: int | None = None,
    active_only: bool = True,
) -> list[dict[str, Any]]:
    base = """
        SELECT TeacherId, InstitutionId, TeacherNo, FirstName, LastName,
               Phone, Email, HireDate, IsActive
        FROM dbo.Teachers
    """
    clauses: list[str] = []
    params: list[Any] = []
    if institution_id is not None:
        clauses.append("InstitutionId = ?")
        params.append(institution_id)
    if active_only:
        clauses.append("IsActive = 1")
    if clauses:
        base += " WHERE " + " AND ".join(clauses)
    base += " ORDER BY TeacherId"
    columns, rows = db.fetch_all(base, tuple(params))
    return db.rows_as_dicts(columns, rows)


def list_courses(
    institution_id: int | None = None,
    active_only: bool = True,
) -> list[dict[str, Any]]:
    base = """
        SELECT CourseId, InstitutionId, CourseCode, CourseName, Description, IsActive
        FROM dbo.Courses
    """
    clauses: list[str] = []
    params: list[Any] = []
    if institution_id is not None:
        clauses.append("InstitutionId = ?")
        params.append(institution_id)
    if active_only:
        clauses.append("IsActive = 1")
    if clauses:
        base += " WHERE " + " AND ".join(clauses)
    base += " ORDER BY CourseId"
    columns, rows = db.fetch_all(base, tuple(params))
    return db.rows_as_dicts(columns, rows)


def list_class_groups(
    institution_id: int | None = None,
    active_only: bool = True,
) -> list[dict[str, Any]]:
    base = """
        SELECT ClassGroupId, InstitutionId, AcademicTermId, CourseId, TeacherId,
               GroupCode, GroupName, Capacity, Classroom, IsActive
        FROM dbo.ClassGroups
    """
    clauses: list[str] = []
    params: list[Any] = []
    if institution_id is not None:
        clauses.append("InstitutionId = ?")
        params.append(institution_id)
    if active_only:
        clauses.append("IsActive = 1")
    if clauses:
        base += " WHERE " + " AND ".join(clauses)
    base += " ORDER BY ClassGroupId"
    columns, rows = db.fetch_all(base, tuple(params))
    return db.rows_as_dicts(columns, rows)


def list_academic_terms(
    institution_id: int | None = None,
    active_only: bool = True,
) -> list[dict[str, Any]]:
    base = """
        SELECT AcademicTermId, InstitutionId, TermName, StartDate, EndDate, IsActive
        FROM dbo.AcademicTerms
    """
    clauses: list[str] = []
    params: list[Any] = []
    if institution_id is not None:
        clauses.append("InstitutionId = ?")
        params.append(institution_id)
    if active_only:
        clauses.append("IsActive = 1")
    if clauses:
        base += " WHERE " + " AND ".join(clauses)
    base += " ORDER BY AcademicTermId"
    columns, rows = db.fetch_all(base, tuple(params))
    return db.rows_as_dicts(columns, rows)


def list_enrollment_details() -> list[dict[str, Any]]:
    sql = """
        SELECT *
        FROM dbo.vw_StudentEnrollmentDetails
        ORDER BY StudentEnrollmentId
    """
    columns, rows = db.fetch_all(sql)
    return db.rows_as_dicts(columns, rows)


def list_teacher_schedule() -> list[dict[str, Any]]:
    sql = """
        SELECT *
        FROM dbo.vw_TeacherSchedule
        ORDER BY TeacherId, ClassGroupId, DayOfWeek
    """
    columns, rows = db.fetch_all(sql)
    return db.rows_as_dicts(columns, rows)


def list_exam_results() -> list[dict[str, Any]]:
    sql = """
        SELECT *
        FROM dbo.vw_StudentExamResults
        ORDER BY ExamId, StudentId
    """
    columns, rows = db.fetch_all(sql)
    return db.rows_as_dicts(columns, rows)


def enroll_student(student_id: int, class_group_id: int) -> None:
    db.execute_non_query(
        "EXEC dbo.usp_EnrollStudentToClassGroup @StudentId=?, @ClassGroupId=?",
        (student_id, class_group_id),
    )


def record_attendance(
    class_group_id: int,
    student_id: int,
    lesson_date: date,
    attendance_status: str,
    note: str | None = None,
) -> None:
    db.execute_non_query(
        "EXEC dbo.usp_RecordAttendance @ClassGroupId=?, @StudentId=?, @LessonDate=?, "
        "@AttendanceStatus=?, @Note=?",
        (class_group_id, student_id, lesson_date, attendance_status, note),
    )


def save_exam_result(
    exam_id: int,
    student_id: int,
    score: Decimal | float,
    note: str | None = None,
) -> None:
    db.execute_non_query(
        "EXEC dbo.usp_SaveExamResult @ExamId=?, @StudentId=?, @Score=?, @Note=?",
        (exam_id, student_id, score, note),
    )
