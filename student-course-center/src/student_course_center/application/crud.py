from __future__ import annotations

from datetime import date, time
from decimal import Decimal
from typing import Any

from student_course_center.infrastructure import db


def _update_by_pk(
    table: str,
    pk_column: str,
    pk_value: int,
    assignments: list[tuple[str, Any]],
) -> None:
    if not assignments:
        return
    cols = ", ".join(f"{c} = ?" for c, _ in assignments)
    params = [v for _, v in assignments] + [pk_value]
    sql = f"UPDATE dbo.{table} SET {cols} WHERE {pk_column} = ?"
    db.execute_non_query(sql, tuple(params))


def list_institutions(active_only: bool = True) -> list[dict[str, Any]]:
    sql = "SELECT * FROM dbo.Institutions"
    if active_only:
        sql += " WHERE IsActive = 1"
    sql += " ORDER BY InstitutionId"
    cols, rows = db.fetch_all(sql)
    return db.rows_as_dicts(cols, rows)


def list_enrollments(
    student_id: int | None = None,
    class_group_id: int | None = None,
) -> list[dict[str, Any]]:
    sql = """
        SELECT StudentEnrollmentId, StudentId, ClassGroupId, EnrollDate,
               EnrollmentStatus, CreatedAt
        FROM dbo.StudentEnrollments
    """
    clauses: list[str] = []
    params: list[Any] = []
    if student_id is not None:
        clauses.append("StudentId = ?")
        params.append(student_id)
    if class_group_id is not None:
        clauses.append("ClassGroupId = ?")
        params.append(class_group_id)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY StudentEnrollmentId"
    cols, rows = db.fetch_all(sql, tuple(params))
    return db.rows_as_dicts(cols, rows)


def list_lesson_schedules(class_group_id: int | None = None) -> list[dict[str, Any]]:
    sql = """
        SELECT LessonScheduleId, ClassGroupId, DayOfWeek, StartTime, EndTime, Room, CreatedAt
        FROM dbo.LessonSchedules
    """
    params: tuple[Any, ...] = ()
    if class_group_id is not None:
        sql += " WHERE ClassGroupId = ?"
        params = (class_group_id,)
    sql += " ORDER BY ClassGroupId, DayOfWeek, StartTime"
    cols, rows = db.fetch_all(sql, params)
    return db.rows_as_dicts(cols, rows)


def list_exams(class_group_id: int | None = None) -> list[dict[str, Any]]:
    sql = """
        SELECT ExamId, ClassGroupId, ExamName, ExamDate, TotalScore, CreatedAt
        FROM dbo.Exams
    """
    params: tuple[Any, ...] = ()
    if class_group_id is not None:
        sql += " WHERE ClassGroupId = ?"
        params = (class_group_id,)
    sql += " ORDER BY ExamDate, ExamId"
    cols, rows = db.fetch_all(sql, params)
    return db.rows_as_dicts(cols, rows)


def list_teacher_courses() -> list[dict[str, Any]]:
    sql = """
        SELECT tc.TeacherCourseId, tc.TeacherId, tc.CourseId, tc.CreatedAt
        FROM dbo.TeacherCourses tc
        ORDER BY tc.TeacherId, tc.CourseId
    """
    cols, rows = db.fetch_all(sql)
    return db.rows_as_dicts(cols, rows)


def list_attendance_records(
    class_group_id: int | None = None,
    student_id: int | None = None,
    lesson_date_from: date | None = None,
    lesson_date_to: date | None = None,
) -> list[dict[str, Any]]:
    sql = """
        SELECT AttendanceRecordId, ClassGroupId, StudentId, LessonDate,
               AttendanceStatus, Note, CreatedAt
        FROM dbo.AttendanceRecords
    """
    clauses: list[str] = []
    params: list[Any] = []
    if class_group_id is not None:
        clauses.append("ClassGroupId = ?")
        params.append(class_group_id)
    if student_id is not None:
        clauses.append("StudentId = ?")
        params.append(student_id)
    if lesson_date_from is not None:
        clauses.append("LessonDate >= ?")
        params.append(lesson_date_from)
    if lesson_date_to is not None:
        clauses.append("LessonDate <= ?")
        params.append(lesson_date_to)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY LessonDate DESC, ClassGroupId, StudentId"
    cols, rows = db.fetch_all(sql, tuple(params))
    return db.rows_as_dicts(cols, rows)


def list_exam_results_raw(
    exam_id: int | None = None,
    student_id: int | None = None,
) -> list[dict[str, Any]]:
    sql = """
        SELECT ExamResultId, ExamId, StudentId, Score, Note, CreatedAt
        FROM dbo.ExamResults
    """
    clauses: list[str] = []
    params: list[Any] = []
    if exam_id is not None:
        clauses.append("ExamId = ?")
        params.append(exam_id)
    if student_id is not None:
        clauses.append("StudentId = ?")
        params.append(student_id)
    if clauses:
        sql += " WHERE " + " AND ".join(clauses)
    sql += " ORDER BY ExamId, StudentId"
    cols, rows = db.fetch_all(sql, tuple(params))
    return db.rows_as_dicts(cols, rows)


def get_student_by_id(student_id: int, *, include_inactive: bool = False) -> list[dict[str, Any]]:
    sql = "SELECT * FROM dbo.Students WHERE StudentId = ?"
    params: list[Any] = [student_id]
    if not include_inactive:
        sql += " AND IsActive = 1"
    cols, rows = db.fetch_all(sql, tuple(params))
    return db.rows_as_dicts(cols, rows)


def get_teacher_by_id(teacher_id: int, *, include_inactive: bool = False) -> list[dict[str, Any]]:
    sql = "SELECT * FROM dbo.Teachers WHERE TeacherId = ?"
    params: list[Any] = [teacher_id]
    if not include_inactive:
        sql += " AND IsActive = 1"
    cols, rows = db.fetch_all(sql, tuple(params))
    return db.rows_as_dicts(cols, rows)


def create_institution(
    name: str,
    phone: str | None = None,
    email: str | None = None,
    address: str | None = None,
) -> None:
    db.execute_non_query(
        "INSERT INTO dbo.Institutions (Name, Phone, Email, Address) VALUES (?, ?, ?, ?)",
        (name, phone, email, address),
    )


def create_student(
    institution_id: int,
    student_no: str,
    first_name: str,
    last_name: str,
    birth_date: date | None = None,
    gender: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    school_name: str | None = None,
    grade_level: int | None = None,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.Students (
            InstitutionId, StudentNo, FirstName, LastName,
            BirthDate, Gender, Phone, Email, SchoolName, GradeLevel
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            institution_id,
            student_no,
            first_name,
            last_name,
            birth_date,
            gender,
            phone,
            email,
            school_name,
            grade_level,
        ),
    )


def create_teacher(
    institution_id: int,
    teacher_no: str,
    first_name: str,
    last_name: str,
    phone: str | None = None,
    email: str | None = None,
    hire_date: date | None = None,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.Teachers (
            InstitutionId, TeacherNo, FirstName, LastName, Phone, Email, HireDate
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (institution_id, teacher_no, first_name, last_name, phone, email, hire_date),
    )


def create_course(
    institution_id: int,
    course_code: str,
    course_name: str,
    description: str | None = None,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.Courses (InstitutionId, CourseCode, CourseName, Description)
        VALUES (?, ?, ?, ?)
        """,
        (institution_id, course_code, course_name, description),
    )


def create_academic_term(
    institution_id: int,
    term_name: str,
    start_date: date,
    end_date: date,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.AcademicTerms (InstitutionId, TermName, StartDate, EndDate)
        VALUES (?, ?, ?, ?)
        """,
        (institution_id, term_name, start_date, end_date),
    )


def create_class_group(
    institution_id: int,
    academic_term_id: int,
    course_id: int,
    teacher_id: int,
    group_code: str,
    group_name: str,
    capacity: int = 20,
    classroom: str | None = None,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.ClassGroups (
            InstitutionId, AcademicTermId, CourseId, TeacherId,
            GroupCode, GroupName, Capacity, Classroom
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            institution_id,
            academic_term_id,
            course_id,
            teacher_id,
            group_code,
            group_name,
            capacity,
            classroom,
        ),
    )


def create_lesson_schedule(
    class_group_id: int,
    day_of_week: int,
    start_time: time,
    end_time: time,
    room: str | None = None,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.LessonSchedules (ClassGroupId, DayOfWeek, StartTime, EndTime, Room)
        VALUES (?, ?, ?, ?, ?)
        """,
        (class_group_id, day_of_week, start_time, end_time, room),
    )


def create_exam(
    class_group_id: int,
    exam_name: str,
    exam_date: date,
    total_score: Decimal | float = 100,
) -> None:
    db.execute_non_query(
        """
        INSERT INTO dbo.Exams (ClassGroupId, ExamName, ExamDate, TotalScore)
        VALUES (?, ?, ?, ?)
        """,
        (class_group_id, exam_name, exam_date, total_score),
    )


def create_teacher_course(teacher_id: int, course_id: int) -> None:
    db.execute_non_query(
        "INSERT INTO dbo.TeacherCourses (TeacherId, CourseId) VALUES (?, ?)",
        (teacher_id, course_id),
    )


def update_student(
    student_id: int,
    *,
    student_no: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    birth_date: date | None = None,
    gender: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    school_name: str | None = None,
    grade_level: int | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if student_no is not None:
        pairs.append(("StudentNo", student_no))
    if first_name is not None:
        pairs.append(("FirstName", first_name))
    if last_name is not None:
        pairs.append(("LastName", last_name))
    if birth_date is not None:
        pairs.append(("BirthDate", birth_date))
    if gender is not None:
        pairs.append(("Gender", gender))
    if phone is not None:
        pairs.append(("Phone", phone))
    if email is not None:
        pairs.append(("Email", email))
    if school_name is not None:
        pairs.append(("SchoolName", school_name))
    if grade_level is not None:
        pairs.append(("GradeLevel", grade_level))
    _update_by_pk("Students", "StudentId", student_id, pairs)


def update_teacher(
    teacher_id: int,
    *,
    teacher_no: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    hire_date: date | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if teacher_no is not None:
        pairs.append(("TeacherNo", teacher_no))
    if first_name is not None:
        pairs.append(("FirstName", first_name))
    if last_name is not None:
        pairs.append(("LastName", last_name))
    if phone is not None:
        pairs.append(("Phone", phone))
    if email is not None:
        pairs.append(("Email", email))
    if hire_date is not None:
        pairs.append(("HireDate", hire_date))
    _update_by_pk("Teachers", "TeacherId", teacher_id, pairs)


def update_course(
    course_id: int,
    *,
    course_code: str | None = None,
    course_name: str | None = None,
    description: str | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if course_code is not None:
        pairs.append(("CourseCode", course_code))
    if course_name is not None:
        pairs.append(("CourseName", course_name))
    if description is not None:
        pairs.append(("Description", description))
    _update_by_pk("Courses", "CourseId", course_id, pairs)


def update_academic_term(
    academic_term_id: int,
    *,
    term_name: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if term_name is not None:
        pairs.append(("TermName", term_name))
    if start_date is not None:
        pairs.append(("StartDate", start_date))
    if end_date is not None:
        pairs.append(("EndDate", end_date))
    _update_by_pk("AcademicTerms", "AcademicTermId", academic_term_id, pairs)


def update_institution(
    institution_id: int,
    *,
    name: str | None = None,
    phone: str | None = None,
    email: str | None = None,
    address: str | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if name is not None:
        pairs.append(("Name", name))
    if phone is not None:
        pairs.append(("Phone", phone))
    if email is not None:
        pairs.append(("Email", email))
    if address is not None:
        pairs.append(("Address", address))
    _update_by_pk("Institutions", "InstitutionId", institution_id, pairs)


def update_class_group(
    class_group_id: int,
    *,
    group_code: str | None = None,
    group_name: str | None = None,
    capacity: int | None = None,
    classroom: str | None = None,
    academic_term_id: int | None = None,
    course_id: int | None = None,
    teacher_id: int | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if group_code is not None:
        pairs.append(("GroupCode", group_code))
    if group_name is not None:
        pairs.append(("GroupName", group_name))
    if capacity is not None:
        pairs.append(("Capacity", capacity))
    if classroom is not None:
        pairs.append(("Classroom", classroom))
    if academic_term_id is not None:
        pairs.append(("AcademicTermId", academic_term_id))
    if course_id is not None:
        pairs.append(("CourseId", course_id))
    if teacher_id is not None:
        pairs.append(("TeacherId", teacher_id))
    _update_by_pk("ClassGroups", "ClassGroupId", class_group_id, pairs)


def update_enrollment_status(student_enrollment_id: int, enrollment_status: str) -> None:
    _update_by_pk(
        "StudentEnrollments",
        "StudentEnrollmentId",
        student_enrollment_id,
        [("EnrollmentStatus", enrollment_status)],
    )


def update_lesson_schedule(
    lesson_schedule_id: int,
    *,
    day_of_week: int | None = None,
    start_time: time | None = None,
    end_time: time | None = None,
    room: str | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if day_of_week is not None:
        pairs.append(("DayOfWeek", day_of_week))
    if start_time is not None:
        pairs.append(("StartTime", start_time))
    if end_time is not None:
        pairs.append(("EndTime", end_time))
    if room is not None:
        pairs.append(("Room", room))
    _update_by_pk("LessonSchedules", "LessonScheduleId", lesson_schedule_id, pairs)


def update_exam(
    exam_id: int,
    *,
    exam_name: str | None = None,
    exam_date: date | None = None,
    total_score: Decimal | float | None = None,
) -> None:
    pairs: list[tuple[str, Any]] = []
    if exam_name is not None:
        pairs.append(("ExamName", exam_name))
    if exam_date is not None:
        pairs.append(("ExamDate", exam_date))
    if total_score is not None:
        pairs.append(("TotalScore", total_score))
    _update_by_pk("Exams", "ExamId", exam_id, pairs)


def deactivate_institution(institution_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Institutions SET IsActive = 0 WHERE InstitutionId = ?",
        (institution_id,),
    )


def deactivate_student(student_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Students SET IsActive = 0 WHERE StudentId = ?",
        (student_id,),
    )


def deactivate_teacher(teacher_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Teachers SET IsActive = 0 WHERE TeacherId = ?",
        (teacher_id,),
    )


def deactivate_course(course_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Courses SET IsActive = 0 WHERE CourseId = ?",
        (course_id,),
    )


def deactivate_academic_term(academic_term_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.AcademicTerms SET IsActive = 0 WHERE AcademicTermId = ?",
        (academic_term_id,),
    )


def deactivate_class_group(class_group_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.ClassGroups SET IsActive = 0 WHERE ClassGroupId = ?",
        (class_group_id,),
    )


def activate_institution(institution_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Institutions SET IsActive = 1 WHERE InstitutionId = ?",
        (institution_id,),
    )


def activate_student(student_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Students SET IsActive = 1 WHERE StudentId = ?",
        (student_id,),
    )


def activate_teacher(teacher_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Teachers SET IsActive = 1 WHERE TeacherId = ?",
        (teacher_id,),
    )


def activate_course(course_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.Courses SET IsActive = 1 WHERE CourseId = ?",
        (course_id,),
    )


def activate_academic_term(academic_term_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.AcademicTerms SET IsActive = 1 WHERE AcademicTermId = ?",
        (academic_term_id,),
    )


def activate_class_group(class_group_id: int) -> None:
    db.execute_non_query(
        "UPDATE dbo.ClassGroups SET IsActive = 1 WHERE ClassGroupId = ?",
        (class_group_id,),
    )


def delete_lesson_schedule(lesson_schedule_id: int) -> None:
    db.execute_non_query(
        "DELETE FROM dbo.LessonSchedules WHERE LessonScheduleId = ?",
        (lesson_schedule_id,),
    )


def delete_teacher_course(teacher_course_id: int) -> None:
    db.execute_non_query(
        "DELETE FROM dbo.TeacherCourses WHERE TeacherCourseId = ?",
        (teacher_course_id,),
    )


def delete_exam_result(exam_result_id: int) -> None:
    db.execute_non_query(
        "DELETE FROM dbo.ExamResults WHERE ExamResultId = ?",
        (exam_result_id,),
    )
