"""Generate synthetic rows via Faker (optional dependency)."""

from __future__ import annotations

import random
from argparse import Namespace
import sys
from datetime import date, time
from decimal import Decimal
from typing import Any

import pyodbc

from student_course_center.application import services
from student_course_center.infrastructure import db


def _require_faker() -> type:
    try:
        from faker import Faker as FakerCls
    except ImportError as e:
        raise RuntimeError(
            'Faker is not installed. Run: pip install "Faker>=24"  or  pip install -e ".[dev]"'
        ) from e
    return FakerCls


def _make_fake(locale: str, seed: int | None) -> Any:
    FakerCls = _require_faker()
    fake = FakerCls(locale)
    if seed is not None:
        FakerCls.seed(seed)
        random.seed(seed)
    fake.unique.clear()
    return fake


def run_seed_faker(args: Namespace) -> int:
    if args.dry_run:
        print(
            "Dry run: would create institution, term, teachers, students, courses, "
            "teacher-course links, class groups, lesson schedules, enrollments (SP), "
            "exams, and exam results (SP)."
        )
        return 0

    fake = _make_fake(args.locale, args.seed)

    inst_name = (fake.company() + " " + fake.city())[:200]
    inst_id = int(
        db.insert_returning_scalar(
            """
            INSERT INTO dbo.Institutions (Name, Phone, Email, Address)
            OUTPUT INSERTED.InstitutionId
            VALUES (?, ?, ?, ?)
            """,
            (
                inst_name,
                fake.phone_number()[:30],
                fake.company_email()[:150],
                fake.address()[:500],
            ),
        )
    )

    y0 = date.today().year
    term_start = date(y0, 9, 1)
    term_end = date(y0 + 1, 6, 30)
    term_name = f"{y0}-{y0 + 1} Faker"
    term_id = int(
        db.insert_returning_scalar(
            """
            INSERT INTO dbo.AcademicTerms (InstitutionId, TermName, StartDate, EndDate)
            OUTPUT INSERTED.AcademicTermId
            VALUES (?, ?, ?, ?)
            """,
            (inst_id, term_name, term_start, term_end),
        )
    )

    teacher_ids: list[int] = []
    for i in range(args.teachers):
        tid = int(
            db.insert_returning_scalar(
                """
                INSERT INTO dbo.Teachers (
                    InstitutionId, TeacherNo, FirstName, LastName, Phone, Email, HireDate
                )
                OUTPUT INSERTED.TeacherId
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    inst_id,
                    f"FT{inst_id}-{i:04d}"[:30],
                    fake.first_name()[:100],
                    fake.last_name()[:100],
                    fake.phone_number()[:30],
                    fake.email()[:150],
                    fake.date_between(start_date="-10y", end_date="today"),
                ),
            )
        )
        teacher_ids.append(tid)

    course_ids: list[int] = []
    for i in range(args.courses):
        code = f"FC{inst_id}_{i:03d}"[:30]
        cid = int(
            db.insert_returning_scalar(
                """
                INSERT INTO dbo.Courses (InstitutionId, CourseCode, CourseName, Description)
                OUTPUT INSERTED.CourseId
                VALUES (?, ?, ?, ?)
                """,
                (
                    inst_id,
                    code,
                    (fake.catch_phrase() or f"Course {i}")[:150],
                    fake.text(max_nb_chars=200)[:500],
                ),
            )
        )
        course_ids.append(cid)

    for cid in course_ids:
        tid = random.choice(teacher_ids)
        try:
            db.execute_non_query(
                "INSERT INTO dbo.TeacherCourses (TeacherId, CourseId) VALUES (?, ?)",
                (tid, cid),
            )
        except pyodbc.IntegrityError:
            pass

    student_ids: list[int] = []
    for i in range(args.students):
        sid = int(
            db.insert_returning_scalar(
                """
                INSERT INTO dbo.Students (
                    InstitutionId, StudentNo, FirstName, LastName,
                    BirthDate, Gender, Phone, Email, SchoolName, GradeLevel
                )
                OUTPUT INSERTED.StudentId
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    inst_id,
                    f"FS{inst_id}-{i:05d}"[:30],
                    fake.first_name()[:100],
                    fake.last_name()[:100],
                    fake.date_of_birth(minimum_age=14, maximum_age=20),
                    random.choice(["F", "M", None]),
                    fake.phone_number()[:30],
                    fake.email()[:150],
                    (fake.company() + " Okul")[:200],
                    random.randint(9, 12),
                ),
            )
        )
        student_ids.append(sid)

    def teachers_for_course(course_id: int) -> list[int]:
        cols, rows = db.fetch_all(
            """
            SELECT TeacherId FROM dbo.TeacherCourses WHERE CourseId = ?
            """,
            (course_id,),
        )
        return [int(r[0]) for r in rows]

    group_ids: list[tuple[int, int]] = []
    for g in range(args.groups):
        course_id = random.choice(course_ids)
        t_candidates = teachers_for_course(course_id)
        if not t_candidates:
            tid = random.choice(teacher_ids)
            db.execute_non_query(
                "INSERT INTO dbo.TeacherCourses (TeacherId, CourseId) VALUES (?, ?)",
                (tid, course_id),
            )
            t_candidates = [tid]
        teacher_id = random.choice(t_candidates)
        cap = random.randint(args.min_capacity, args.max_capacity)
        gid = int(
            db.insert_returning_scalar(
                """
                INSERT INTO dbo.ClassGroups (
                    InstitutionId, AcademicTermId, CourseId, TeacherId,
                    GroupCode, GroupName, Capacity, Classroom
                )
                OUTPUT INSERTED.ClassGroupId
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    inst_id,
                    term_id,
                    course_id,
                    teacher_id,
                    f"FG{inst_id}-{g:03d}-{random.randint(100, 999)}"[:30],
                    (fake.catch_phrase() or f"Group {g}")[:150],
                    cap,
                    fake.bothify(text="??#", letters="ABCD")[:50],
                ),
            )
        )
        group_ids.append((gid, cap))

    time_slots = [
        (time(9, 0), time(10, 30)),
        (time(11, 0), time(12, 30)),
        (time(14, 0), time(15, 30)),
    ]
    for gid, _cap in group_ids:
        for d in random.sample(range(1, 8), k=min(args.schedules_per_group, 7)):
            st, et = random.choice(time_slots)
            try:
                db.execute_non_query(
                    """
                    INSERT INTO dbo.LessonSchedules (ClassGroupId, DayOfWeek, StartTime, EndTime, Room)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (gid, d, st, et, fake.bothify(text="R-##", letters="AB")[:50]),
                )
            except pyodbc.Error:
                pass

    for gid, cap in group_ids:
        picks = random.sample(student_ids, k=min(cap, len(student_ids)))
        for sid in picks:
            try:
                services.enroll_student(sid, gid)
            except pyodbc.Error:
                pass

    exam_ids: list[tuple[int, int]] = []
    for gid, _ in group_ids:
        for _e in range(args.exams_per_group):
            total = Decimal(str(random.choice([50, 60, 100])))
            eid = int(
                db.insert_returning_scalar(
                    """
                    INSERT INTO dbo.Exams (ClassGroupId, ExamName, ExamDate, TotalScore)
                    OUTPUT INSERTED.ExamId
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        gid,
                        (fake.sentence(nb_words=3) or "Quiz")[:150].rstrip("."),
                        fake.date_between(start_date=term_start, end_date=term_end),
                        total,
                    ),
                )
            )
            exam_ids.append((eid, gid))

    for exam_id, class_group_id in exam_ids:
        cols, rows = db.fetch_all(
            """
            SELECT StudentId FROM dbo.StudentEnrollments
            WHERE ClassGroupId = ? AND EnrollmentStatus = N'Active'
            """,
            (class_group_id,),
        )
        enrolled = [int(r[0]) for r in rows]
        cols2, rows2 = db.fetch_all(
            "SELECT TotalScore FROM dbo.Exams WHERE ExamId = ?",
            (exam_id,),
        )
        if not rows2:
            continue
        total = Decimal(str(rows2[0][0]))
        for sid in enrolled:
            if random.random() < args.exam_skip_rate:
                continue
            score = Decimal(str(random.randint(0, int(total))))
            try:
                services.save_exam_result(
                    exam_id,
                    sid,
                    score,
                    fake.sentence(nb_words=5)[:300] if random.random() > 0.7 else None,
                )
            except pyodbc.Error:
                pass

    print(
        f"Seed complete. InstitutionId={inst_id}, AcademicTermId={term_id}, "
        f"students={len(student_ids)}, teachers={len(teacher_ids)}, courses={len(course_ids)}, "
        f"class_groups={len(group_ids)}."
    )
    return 0


def register_seed_faker_parser(seed_sub: Any) -> None:
    p = seed_sub.add_parser(
        "faker",
        help="Insert synthetic data using Faker (requires: pip install Faker)",
    )
    p.add_argument(
        "--locale",
        default="tr_TR",
        help="Faker locale (default: tr_TR)",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible data",
    )
    p.add_argument("--students", type=int, default=12, metavar="N")
    p.add_argument("--teachers", type=int, default=3, metavar="N")
    p.add_argument("--courses", type=int, default=4, metavar="N")
    p.add_argument("--groups", type=int, default=3, metavar="N", dest="groups")
    p.add_argument("--schedules-per-group", type=int, default=2, metavar="N")
    p.add_argument("--exams-per-group", type=int, default=1, metavar="N")
    p.add_argument("--min-capacity", type=int, default=15)
    p.add_argument("--max-capacity", type=int, default=28)
    p.add_argument(
        "--exam-skip-rate",
        type=float,
        default=0.15,
        metavar="P",
        help="Probability to skip a student's exam result (0=everyone gets a score, 1=no scores)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without touching the database",
    )
    p.set_defaults(handler=run_seed_faker)
