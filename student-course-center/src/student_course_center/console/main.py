from __future__ import annotations

import argparse
import sys
from datetime import date, time
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Sequence

import pyodbc
from tabulate import tabulate

from student_course_center.application import crud, services
from student_course_center.application.faker_seed import register_seed_faker_parser
from student_course_center.domain.constants import ATTENDANCE_STATUSES, ENROLLMENT_STATUSES


def _parse_time(s: str) -> time:
    return time.fromisoformat(s)


def _print_table(rows: Sequence[dict[str, Any]]) -> None:
    if not rows:
        print("(no rows)")
        return
    headers = list(rows[0].keys())
    table = [[row.get(h) for h in headers] for row in rows]
    print(tabulate(table, headers=headers, tablefmt="simple"))


def _add_institution_filter(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--institution",
        type=int,
        default=None,
        metavar="ID",
        help="Filter by InstitutionId",
    )
    p.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include rows where IsActive = 0",
    )


def _cmd_ping(_: argparse.Namespace) -> int:
    rows = services.ping()
    _print_table(rows)
    return 0


def _cmd_list_students(args: argparse.Namespace) -> int:
    rows = services.list_students(
        institution_id=args.institution,
        active_only=not args.include_inactive,
    )
    _print_table(rows)
    return 0


def _cmd_list_teachers(args: argparse.Namespace) -> int:
    rows = services.list_teachers(
        institution_id=args.institution,
        active_only=not args.include_inactive,
    )
    _print_table(rows)
    return 0


def _cmd_list_courses(args: argparse.Namespace) -> int:
    rows = services.list_courses(
        institution_id=args.institution,
        active_only=not args.include_inactive,
    )
    _print_table(rows)
    return 0


def _cmd_list_class_groups(args: argparse.Namespace) -> int:
    rows = services.list_class_groups(
        institution_id=args.institution,
        active_only=not args.include_inactive,
    )
    _print_table(rows)
    return 0


def _cmd_list_terms(args: argparse.Namespace) -> int:
    rows = services.list_academic_terms(
        institution_id=args.institution,
        active_only=not args.include_inactive,
    )
    _print_table(rows)
    return 0


def _cmd_list_enrollment_details(_: argparse.Namespace) -> int:
    _print_table(services.list_enrollment_details())
    return 0


def _cmd_list_teacher_schedule(_: argparse.Namespace) -> int:
    _print_table(services.list_teacher_schedule())
    return 0


def _cmd_list_exam_results(_: argparse.Namespace) -> int:
    _print_table(services.list_exam_results())
    return 0


def _cmd_list_institutions(args: argparse.Namespace) -> int:
    _print_table(crud.list_institutions(active_only=not args.include_inactive))
    return 0


def _cmd_list_enrollments(args: argparse.Namespace) -> int:
    _print_table(
        crud.list_enrollments(
            student_id=args.student,
            class_group_id=args.group,
        )
    )
    return 0


def _cmd_list_lesson_schedules(args: argparse.Namespace) -> int:
    _print_table(crud.list_lesson_schedules(class_group_id=args.group))
    return 0


def _cmd_list_exams(args: argparse.Namespace) -> int:
    _print_table(crud.list_exams(class_group_id=args.group))
    return 0


def _cmd_list_teacher_courses(_: argparse.Namespace) -> int:
    _print_table(crud.list_teacher_courses())
    return 0


def _cmd_list_attendance_records(args: argparse.Namespace) -> int:
    _print_table(
        crud.list_attendance_records(
            class_group_id=args.group,
            student_id=args.student,
            lesson_date_from=args.from_date,
            lesson_date_to=args.to_date,
        )
    )
    return 0


def _cmd_list_exam_results_rows(args: argparse.Namespace) -> int:
    _print_table(
        crud.list_exam_results_raw(
            exam_id=args.exam,
            student_id=args.student,
        )
    )
    return 0


def _cmd_show_student(args: argparse.Namespace) -> int:
    rows = crud.get_student_by_id(args.id, include_inactive=args.include_inactive)
    if not rows:
        print("Student not found.", file=sys.stderr)
        return 2
    _print_table(rows)
    return 0


def _cmd_show_teacher(args: argparse.Namespace) -> int:
    rows = crud.get_teacher_by_id(args.id, include_inactive=args.include_inactive)
    if not rows:
        print("Teacher not found.", file=sys.stderr)
        return 2
    _print_table(rows)
    return 0


def _cmd_enroll(args: argparse.Namespace) -> int:
    services.enroll_student(args.student, args.group)
    print("Enrollment created.")
    return 0


def _cmd_attendance(args: argparse.Namespace) -> int:
    status = args.status.strip()
    if status not in ATTENDANCE_STATUSES:
        print(
            f"Invalid status {status!r}. Use one of: {', '.join(sorted(ATTENDANCE_STATUSES))}",
            file=sys.stderr,
        )
        return 2
    services.record_attendance(
        args.group,
        args.student,
        args.lesson_date,
        status,
        args.note,
    )
    print("Attendance saved.")
    return 0


def _cmd_exam_result(args: argparse.Namespace) -> int:
    try:
        score = Decimal(str(args.score))
    except InvalidOperation:
        print("Invalid score.", file=sys.stderr)
        return 2
    services.save_exam_result(args.exam, args.student, score, args.note)
    print("Exam result saved.")
    return 0


def _cmd_create_institution(args: argparse.Namespace) -> int:
    crud.create_institution(args.name, args.phone, args.email, args.address)
    print("Institution created.")
    return 0


def _cmd_create_student(args: argparse.Namespace) -> int:
    crud.create_student(
        args.institution,
        args.student_no,
        args.first_name,
        args.last_name,
        args.birth_date,
        args.gender,
        args.phone,
        args.email,
        args.school_name,
        args.grade_level,
    )
    print("Student created.")
    return 0


def _cmd_create_teacher(args: argparse.Namespace) -> int:
    crud.create_teacher(
        args.institution,
        args.teacher_no,
        args.first_name,
        args.last_name,
        args.phone,
        args.email,
        args.hire_date,
    )
    print("Teacher created.")
    return 0


def _cmd_create_course(args: argparse.Namespace) -> int:
    crud.create_course(
        args.institution,
        args.code,
        args.name,
        args.description,
    )
    print("Course created.")
    return 0


def _cmd_create_academic_term(args: argparse.Namespace) -> int:
    crud.create_academic_term(
        args.institution,
        args.name,
        args.start,
        args.end,
    )
    print("Academic term created.")
    return 0


def _cmd_create_class_group(args: argparse.Namespace) -> int:
    crud.create_class_group(
        args.institution,
        args.term,
        args.course,
        args.teacher,
        args.code,
        args.name,
        args.capacity,
        args.classroom,
    )
    print("Class group created.")
    return 0


def _cmd_create_lesson_schedule(args: argparse.Namespace) -> int:
    crud.create_lesson_schedule(
        args.group,
        args.day,
        args.start,
        args.end,
        args.room,
    )
    print("Lesson schedule created.")
    return 0


def _cmd_create_exam(args: argparse.Namespace) -> int:
    crud.create_exam(args.group, args.name, args.date, args.total)
    print("Exam created.")
    return 0


def _cmd_create_teacher_course(args: argparse.Namespace) -> int:
    crud.create_teacher_course(args.teacher, args.course)
    print("Teacher-course link created.")
    return 0


def _cmd_update_student(args: argparse.Namespace) -> int:
    fields = {
        "student_no": args.student_no,
        "first_name": args.first_name,
        "last_name": args.last_name,
        "birth_date": args.birth_date,
        "gender": args.gender,
        "phone": args.phone,
        "email": args.email,
        "school_name": args.school_name,
        "grade_level": args.grade_level,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_student(args.id, **fields)
    print("Student updated.")
    return 0


def _cmd_update_teacher(args: argparse.Namespace) -> int:
    fields = {
        "teacher_no": args.teacher_no,
        "first_name": args.first_name,
        "last_name": args.last_name,
        "phone": args.phone,
        "email": args.email,
        "hire_date": args.hire_date,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_teacher(args.id, **fields)
    print("Teacher updated.")
    return 0


def _cmd_update_course(args: argparse.Namespace) -> int:
    fields = {
        "course_code": args.code,
        "course_name": args.name,
        "description": args.description,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_course(args.id, **fields)
    print("Course updated.")
    return 0


def _cmd_update_academic_term(args: argparse.Namespace) -> int:
    fields = {
        "term_name": args.name,
        "start_date": args.start,
        "end_date": args.end,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_academic_term(args.id, **fields)
    print("Academic term updated.")
    return 0


def _cmd_update_institution(args: argparse.Namespace) -> int:
    fields = {
        "name": args.name,
        "phone": args.phone,
        "email": args.email,
        "address": args.address,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_institution(args.id, **fields)
    print("Institution updated.")
    return 0


def _cmd_update_class_group(args: argparse.Namespace) -> int:
    fields = {
        "group_code": args.code,
        "group_name": args.name,
        "capacity": args.capacity,
        "classroom": args.classroom,
        "academic_term_id": args.term,
        "course_id": args.course,
        "teacher_id": args.teacher,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_class_group(args.id, **fields)
    print("Class group updated.")
    return 0


def _cmd_update_enrollment(args: argparse.Namespace) -> int:
    status = args.status.strip()
    if status not in ENROLLMENT_STATUSES:
        print(
            f"Invalid status {status!r}. Use one of: {', '.join(sorted(ENROLLMENT_STATUSES))}",
            file=sys.stderr,
        )
        return 2
    crud.update_enrollment_status(args.id, status)
    print("Enrollment updated.")
    return 0


def _cmd_update_lesson_schedule(args: argparse.Namespace) -> int:
    fields = {
        "day_of_week": args.day,
        "start_time": args.start,
        "end_time": args.end,
        "room": args.room,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_lesson_schedule(args.id, **fields)
    print("Lesson schedule updated.")
    return 0


def _cmd_update_exam(args: argparse.Namespace) -> int:
    fields = {
        "exam_name": args.name,
        "exam_date": args.date,
        "total_score": args.total,
    }
    if not any(v is not None for v in fields.values()):
        print("Provide at least one field to update.", file=sys.stderr)
        return 2
    crud.update_exam(args.id, **fields)
    print("Exam updated.")
    return 0


def _cmd_deactivate_institution(args: argparse.Namespace) -> int:
    crud.deactivate_institution(args.id)
    print("Institution deactivated (IsActive=0).")
    return 0


def _cmd_deactivate_student(args: argparse.Namespace) -> int:
    crud.deactivate_student(args.id)
    print("Student deactivated (IsActive=0).")
    return 0


def _cmd_deactivate_teacher(args: argparse.Namespace) -> int:
    crud.deactivate_teacher(args.id)
    print("Teacher deactivated (IsActive=0).")
    return 0


def _cmd_deactivate_course(args: argparse.Namespace) -> int:
    crud.deactivate_course(args.id)
    print("Course deactivated (IsActive=0).")
    return 0


def _cmd_deactivate_academic_term(args: argparse.Namespace) -> int:
    crud.deactivate_academic_term(args.id)
    print("Academic term deactivated (IsActive=0).")
    return 0


def _cmd_deactivate_class_group(args: argparse.Namespace) -> int:
    crud.deactivate_class_group(args.id)
    print("Class group deactivated (IsActive=0).")
    return 0


def _cmd_delete_lesson_schedule(args: argparse.Namespace) -> int:
    crud.delete_lesson_schedule(args.id)
    print("Lesson schedule deleted.")
    return 0


def _cmd_delete_teacher_course(args: argparse.Namespace) -> int:
    crud.delete_teacher_course(args.id)
    print("Teacher-course link deleted.")
    return 0


def _cmd_delete_exam_result(args: argparse.Namespace) -> int:
    crud.delete_exam_result(args.id)
    print("Exam result row deleted (dbo.ExamResults).")
    return 0


def _cmd_activate_institution(args: argparse.Namespace) -> int:
    crud.activate_institution(args.id)
    print("Institution activated (IsActive=1).")
    return 0


def _cmd_activate_student(args: argparse.Namespace) -> int:
    crud.activate_student(args.id)
    print("Student activated (IsActive=1).")
    return 0


def _cmd_activate_teacher(args: argparse.Namespace) -> int:
    crud.activate_teacher(args.id)
    print("Teacher activated (IsActive=1).")
    return 0


def _cmd_activate_course(args: argparse.Namespace) -> int:
    crud.activate_course(args.id)
    print("Course activated (IsActive=1).")
    return 0


def _cmd_activate_academic_term(args: argparse.Namespace) -> int:
    crud.activate_academic_term(args.id)
    print("Academic term activated (IsActive=1).")
    return 0


def _cmd_activate_class_group(args: argparse.Namespace) -> int:
    crud.activate_class_group(args.id)
    print("Class group activated (IsActive=1).")
    return 0


def _run(cmd: Callable[[argparse.Namespace], int], args: argparse.Namespace) -> int:
    try:
        return cmd(args)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2
    except pyodbc.Error as e:
        print("Database error:", e, file=sys.stderr)
        return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="scc",
        description="Student Course Center — SQL Server console client",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ping = sub.add_parser("ping", help="Test database connectivity")
    p_ping.set_defaults(handler=_cmd_ping)

    seed_p = sub.add_parser("seed", help="Load synthetic / test data")
    seed_sub = seed_p.add_subparsers(dest="seed_cmd", required=True)
    register_seed_faker_parser(seed_sub)

    show_p = sub.add_parser("show", help="Single-row detail (student / teacher)")
    show_sub = show_p.add_subparsers(dest="show_entity", required=True)

    p_show_stu = show_sub.add_parser("student", help="Student by StudentId")
    p_show_stu.add_argument("--id", type=int, required=True)
    p_show_stu.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include row if IsActive = 0",
    )
    p_show_stu.set_defaults(handler=_cmd_show_student)

    p_show_teach = show_sub.add_parser("teacher", help="Teacher by TeacherId")
    p_show_teach.add_argument("--id", type=int, required=True)
    p_show_teach.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include row if IsActive = 0",
    )
    p_show_teach.set_defaults(handler=_cmd_show_teacher)

    list_p = sub.add_parser("list", help="List entities")
    list_sub = list_p.add_subparsers(dest="entity", required=True)

    p_stu = list_sub.add_parser("students", help="List students")
    _add_institution_filter(p_stu)
    p_stu.set_defaults(handler=_cmd_list_students)

    p_teach = list_sub.add_parser("teachers", help="List teachers")
    _add_institution_filter(p_teach)
    p_teach.set_defaults(handler=_cmd_list_teachers)

    p_courses = list_sub.add_parser("courses", help="List courses")
    _add_institution_filter(p_courses)
    p_courses.set_defaults(handler=_cmd_list_courses)

    p_groups = list_sub.add_parser("class-groups", help="List class groups")
    _add_institution_filter(p_groups)
    p_groups.set_defaults(handler=_cmd_list_class_groups)

    p_terms = list_sub.add_parser("academic-terms", help="List academic terms")
    _add_institution_filter(p_terms)
    p_terms.set_defaults(handler=_cmd_list_terms)

    p_inst = list_sub.add_parser("institutions", help="List institutions")
    p_inst.add_argument(
        "--include-inactive",
        action="store_true",
        help="Include IsActive = 0",
    )
    p_inst.set_defaults(handler=_cmd_list_institutions)

    p_enr = list_sub.add_parser("enrollments", help="List StudentEnrollments rows")
    p_enr.add_argument("--student", type=int, default=None, metavar="ID")
    p_enr.add_argument("--group", type=int, default=None, metavar="ID", dest="group")
    p_enr.set_defaults(handler=_cmd_list_enrollments)

    p_ls = list_sub.add_parser("lesson-schedules", help="List LessonSchedules")
    p_ls.add_argument("--group", type=int, default=None, metavar="ID", dest="group")
    p_ls.set_defaults(handler=_cmd_list_lesson_schedules)

    p_exl = list_sub.add_parser("exams", help="List Exams")
    p_exl.add_argument("--group", type=int, default=None, metavar="ID", dest="group")
    p_exl.set_defaults(handler=_cmd_list_exams)

    p_tc = list_sub.add_parser("teacher-courses", help="List TeacherCourses")
    p_tc.set_defaults(handler=_cmd_list_teacher_courses)

    p_attl = list_sub.add_parser(
        "attendance-records",
        help="List dbo.AttendanceRecords (raw rows)",
    )
    p_attl.add_argument("--group", type=int, default=None, metavar="ID", dest="group")
    p_attl.add_argument("--student", type=int, default=None, metavar="ID")
    p_attl.add_argument(
        "--from-date",
        type=date.fromisoformat,
        default=None,
        dest="from_date",
        metavar="DATE",
    )
    p_attl.add_argument(
        "--to-date",
        type=date.fromisoformat,
        default=None,
        dest="to_date",
        metavar="DATE",
    )
    p_attl.set_defaults(handler=_cmd_list_attendance_records)

    p_err = list_sub.add_parser(
        "exam-results-rows",
        help="List dbo.ExamResults (not the vw_StudentExamResults view)",
    )
    p_err.add_argument("--exam", type=int, default=None, metavar="ID")
    p_err.add_argument("--student", type=int, default=None, metavar="ID")
    p_err.set_defaults(handler=_cmd_list_exam_results_rows)

    p_end = list_sub.add_parser(
        "enrollment-details",
        help="List vw_StudentEnrollmentDetails",
    )
    p_end.set_defaults(handler=_cmd_list_enrollment_details)

    p_ts = list_sub.add_parser("teacher-schedule", help="List vw_TeacherSchedule")
    p_ts.set_defaults(handler=_cmd_list_teacher_schedule)

    p_er = list_sub.add_parser(
        "exam-results",
        help="List vw_StudentExamResults (denormalized view)",
    )
    p_er.set_defaults(handler=_cmd_list_exam_results)

    create_p = sub.add_parser("create", help="Insert rows (direct SQL)")
    create_sub = create_p.add_subparsers(dest="create_entity", required=True)

    pci = create_sub.add_parser("institution", help="Create institution")
    pci.add_argument("--name", required=True)
    pci.add_argument("--phone", default=None)
    pci.add_argument("--email", default=None)
    pci.add_argument("--address", default=None)
    pci.set_defaults(handler=_cmd_create_institution)

    pcs = create_sub.add_parser("student", help="Create student")
    pcs.add_argument("--institution", type=int, required=True)
    pcs.add_argument("--student-no", required=True, dest="student_no")
    pcs.add_argument("--first-name", required=True, dest="first_name")
    pcs.add_argument("--last-name", required=True, dest="last_name")
    pcs.add_argument("--birth-date", type=date.fromisoformat, default=None, dest="birth_date")
    pcs.add_argument("--gender", default=None)
    pcs.add_argument("--phone", default=None)
    pcs.add_argument("--email", default=None)
    pcs.add_argument("--school-name", default=None, dest="school_name")
    pcs.add_argument("--grade-level", type=int, default=None, dest="grade_level")
    pcs.set_defaults(handler=_cmd_create_student)

    pct = create_sub.add_parser("teacher", help="Create teacher")
    pct.add_argument("--institution", type=int, required=True)
    pct.add_argument("--teacher-no", required=True, dest="teacher_no")
    pct.add_argument("--first-name", required=True, dest="first_name")
    pct.add_argument("--last-name", required=True, dest="last_name")
    pct.add_argument("--phone", default=None)
    pct.add_argument("--email", default=None)
    pct.add_argument("--hire-date", type=date.fromisoformat, default=None, dest="hire_date")
    pct.set_defaults(handler=_cmd_create_teacher)

    pcc = create_sub.add_parser("course", help="Create course")
    pcc.add_argument("--institution", type=int, required=True)
    pcc.add_argument("--code", required=True)
    pcc.add_argument("--name", required=True)
    pcc.add_argument("--description", default=None)
    pcc.set_defaults(handler=_cmd_create_course)

    pcat = create_sub.add_parser("academic-term", help="Create academic term")
    pcat.add_argument("--institution", type=int, required=True)
    pcat.add_argument("--name", required=True)
    pcat.add_argument("--start", type=date.fromisoformat, required=True)
    pcat.add_argument("--end", type=date.fromisoformat, required=True)
    pcat.set_defaults(handler=_cmd_create_academic_term)

    pcg = create_sub.add_parser("class-group", help="Create class group")
    pcg.add_argument("--institution", type=int, required=True)
    pcg.add_argument("--term", type=int, required=True)
    pcg.add_argument("--course", type=int, required=True)
    pcg.add_argument("--teacher", type=int, required=True)
    pcg.add_argument("--code", required=True)
    pcg.add_argument("--name", required=True)
    pcg.add_argument("--capacity", type=int, default=20)
    pcg.add_argument("--classroom", default=None)
    pcg.set_defaults(handler=_cmd_create_class_group)

    pcl = create_sub.add_parser("lesson-schedule", help="Create lesson schedule")
    pcl.add_argument("--group", type=int, required=True, dest="group")
    pcl.add_argument("--day", type=int, required=True, help="DayOfWeek 1-7")
    pcl.add_argument("--start", type=_parse_time, required=True)
    pcl.add_argument("--end", type=_parse_time, required=True)
    pcl.add_argument("--room", default=None)
    pcl.set_defaults(handler=_cmd_create_lesson_schedule)

    pce = create_sub.add_parser("exam", help="Create exam row")
    pce.add_argument("--group", type=int, required=True, dest="group")
    pce.add_argument("--name", required=True)
    pce.add_argument("--date", type=date.fromisoformat, required=True)
    pce.add_argument("--total", type=Decimal, default=Decimal("100"))
    pce.set_defaults(handler=_cmd_create_exam)

    pctl = create_sub.add_parser("teacher-course", help="Link teacher to course")
    pctl.add_argument("--teacher", type=int, required=True)
    pctl.add_argument("--course", type=int, required=True)
    pctl.set_defaults(handler=_cmd_create_teacher_course)

    update_p = sub.add_parser("update", help="Update rows (direct SQL)")
    update_sub = update_p.add_subparsers(dest="update_entity", required=True)

    pus = update_sub.add_parser("student")
    pus.add_argument("--id", type=int, required=True)
    pus.add_argument("--student-no", default=None, dest="student_no")
    pus.add_argument("--first-name", default=None, dest="first_name")
    pus.add_argument("--last-name", default=None, dest="last_name")
    pus.add_argument("--birth-date", type=date.fromisoformat, default=None, dest="birth_date")
    pus.add_argument("--gender", default=None)
    pus.add_argument("--phone", default=None)
    pus.add_argument("--email", default=None)
    pus.add_argument("--school-name", default=None, dest="school_name")
    pus.add_argument("--grade-level", type=int, default=None, dest="grade_level")
    pus.set_defaults(handler=_cmd_update_student)

    put = update_sub.add_parser("teacher")
    put.add_argument("--id", type=int, required=True)
    put.add_argument("--teacher-no", default=None, dest="teacher_no")
    put.add_argument("--first-name", default=None, dest="first_name")
    put.add_argument("--last-name", default=None, dest="last_name")
    put.add_argument("--phone", default=None)
    put.add_argument("--email", default=None)
    put.add_argument("--hire-date", type=date.fromisoformat, default=None, dest="hire_date")
    put.set_defaults(handler=_cmd_update_teacher)

    puc = update_sub.add_parser("course")
    puc.add_argument("--id", type=int, required=True)
    puc.add_argument("--code", default=None)
    puc.add_argument("--name", default=None)
    puc.add_argument("--description", default=None)
    puc.set_defaults(handler=_cmd_update_course)

    puat = update_sub.add_parser("academic-term")
    puat.add_argument("--id", type=int, required=True)
    puat.add_argument("--name", default=None)
    puat.add_argument("--start", type=date.fromisoformat, default=None)
    puat.add_argument("--end", type=date.fromisoformat, default=None)
    puat.set_defaults(handler=_cmd_update_academic_term)

    pui = update_sub.add_parser("institution")
    pui.add_argument("--id", type=int, required=True)
    pui.add_argument("--name", default=None)
    pui.add_argument("--phone", default=None)
    pui.add_argument("--email", default=None)
    pui.add_argument("--address", default=None)
    pui.set_defaults(handler=_cmd_update_institution)

    pug = update_sub.add_parser("class-group")
    pug.add_argument("--id", type=int, required=True)
    pug.add_argument("--code", default=None)
    pug.add_argument("--name", default=None)
    pug.add_argument("--capacity", type=int, default=None)
    pug.add_argument("--classroom", default=None)
    pug.add_argument("--term", type=int, default=None)
    pug.add_argument("--course", type=int, default=None)
    pug.add_argument("--teacher", type=int, default=None)
    pug.set_defaults(handler=_cmd_update_class_group)

    pue = update_sub.add_parser("enrollment", help="Set EnrollmentStatus (not new enroll)")
    pue.add_argument("--id", type=int, required=True, help="StudentEnrollmentId")
    pue.add_argument("--status", required=True)
    pue.set_defaults(handler=_cmd_update_enrollment)

    pul = update_sub.add_parser("lesson-schedule")
    pul.add_argument("--id", type=int, required=True)
    pul.add_argument("--day", type=int, default=None)
    pul.add_argument("--start", type=_parse_time, default=None)
    pul.add_argument("--end", type=_parse_time, default=None)
    pul.add_argument("--room", default=None)
    pul.set_defaults(handler=_cmd_update_lesson_schedule)

    puex = update_sub.add_parser("exam")
    puex.add_argument("--id", type=int, required=True)
    puex.add_argument("--name", default=None)
    puex.add_argument("--date", type=date.fromisoformat, default=None)
    puex.add_argument("--total", type=Decimal, default=None)
    puex.set_defaults(handler=_cmd_update_exam)

    deact_p = sub.add_parser("deactivate", help="Set IsActive = 0")
    deact_sub = deact_p.add_subparsers(dest="deactivate_entity", required=True)

    d_i = deact_sub.add_parser("institution")
    d_i.add_argument("--id", type=int, required=True)
    d_i.set_defaults(handler=_cmd_deactivate_institution)

    d_s = deact_sub.add_parser("student")
    d_s.add_argument("--id", type=int, required=True)
    d_s.set_defaults(handler=_cmd_deactivate_student)

    d_t = deact_sub.add_parser("teacher")
    d_t.add_argument("--id", type=int, required=True)
    d_t.set_defaults(handler=_cmd_deactivate_teacher)

    d_c = deact_sub.add_parser("course")
    d_c.add_argument("--id", type=int, required=True)
    d_c.set_defaults(handler=_cmd_deactivate_course)

    d_at = deact_sub.add_parser("academic-term")
    d_at.add_argument("--id", type=int, required=True)
    d_at.set_defaults(handler=_cmd_deactivate_academic_term)

    d_cg = deact_sub.add_parser("class-group")
    d_cg.add_argument("--id", type=int, required=True)
    d_cg.set_defaults(handler=_cmd_deactivate_class_group)

    act_p = sub.add_parser("activate", help="Set IsActive = 1")
    act_sub = act_p.add_subparsers(dest="activate_entity", required=True)

    a_i = act_sub.add_parser("institution")
    a_i.add_argument("--id", type=int, required=True)
    a_i.set_defaults(handler=_cmd_activate_institution)

    a_s = act_sub.add_parser("student")
    a_s.add_argument("--id", type=int, required=True)
    a_s.set_defaults(handler=_cmd_activate_student)

    a_t = act_sub.add_parser("teacher")
    a_t.add_argument("--id", type=int, required=True)
    a_t.set_defaults(handler=_cmd_activate_teacher)

    a_c = act_sub.add_parser("course")
    a_c.add_argument("--id", type=int, required=True)
    a_c.set_defaults(handler=_cmd_activate_course)

    a_at = act_sub.add_parser("academic-term")
    a_at.add_argument("--id", type=int, required=True)
    a_at.set_defaults(handler=_cmd_activate_academic_term)

    a_cg = act_sub.add_parser("class-group")
    a_cg.add_argument("--id", type=int, required=True)
    a_cg.set_defaults(handler=_cmd_activate_class_group)

    del_p = sub.add_parser(
        "delete",
        help="Hard delete (LessonSchedules, TeacherCourses, ExamResults row)",
    )
    del_sub = del_p.add_subparsers(dest="delete_entity", required=True)

    dd_ls = del_sub.add_parser("lesson-schedule")
    dd_ls.add_argument("--id", type=int, required=True)
    dd_ls.set_defaults(handler=_cmd_delete_lesson_schedule)

    dd_tc = del_sub.add_parser("teacher-course")
    dd_tc.add_argument("--id", type=int, required=True)
    dd_tc.set_defaults(handler=_cmd_delete_teacher_course)

    dd_er = del_sub.add_parser(
        "exam-result",
        help="Delete dbo.ExamResults row by ExamResultId (not upsert SP)",
    )
    dd_er.add_argument("--id", type=int, required=True)
    dd_er.set_defaults(handler=_cmd_delete_exam_result)

    p_enroll = sub.add_parser("enroll", help="Enroll student via usp_EnrollStudentToClassGroup")
    p_enroll.add_argument("--student", type=int, required=True, metavar="ID")
    p_enroll.add_argument("--group", type=int, required=True, metavar="ID", dest="group")
    p_enroll.set_defaults(handler=_cmd_enroll)

    p_att = sub.add_parser("attendance", help="Record attendance via usp_RecordAttendance")
    p_att.add_argument("--group", type=int, required=True, metavar="ID", dest="group")
    p_att.add_argument("--student", type=int, required=True, metavar="ID")
    p_att.add_argument("--date", type=date.fromisoformat, required=True, dest="lesson_date")
    p_att.add_argument("--status", type=str, required=True)
    p_att.add_argument("--note", type=str, default=None)
    p_att.set_defaults(handler=_cmd_attendance)

    p_ex = sub.add_parser("exam-result", help="Save exam result via usp_SaveExamResult")
    p_ex.add_argument("--exam", type=int, required=True, metavar="ID")
    p_ex.add_argument("--student", type=int, required=True, metavar="ID")
    p_ex.add_argument("--score", type=str, required=True)
    p_ex.add_argument("--note", type=str, default=None)
    p_ex.set_defaults(handler=_cmd_exam_result)

    args = parser.parse_args(argv)
    handler: Callable[[argparse.Namespace], int] = args.handler
    return _run(handler, args)


if __name__ == "__main__":
    raise SystemExit(main())
