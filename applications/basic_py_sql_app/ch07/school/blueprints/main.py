from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from school.exceptions import ValidationError
from school.forms import DepartmentForm, StudentForm
from school.services import DepartmentService, StudentService

bp = Blueprint("school", __name__)


@bp.route("/")
def home():
    dept_svc = DepartmentService()
    st_svc = StudentService()
    return render_template(
        "school/home.html",
        department_count=len(dept_svc.list_departments()),
        student_count=len(st_svc.list_students()),
    )


@bp.route("/departments", methods=["GET", "POST"], strict_slashes=False)
def department_list():
    template = "school/department_list.html"
    dept_svc = DepartmentService()
    departments = dept_svc.list_departments()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            form = DepartmentForm(formdata=request.form, prefix="dept_create")
            if form.validate():
                try:
                    dept_svc.create_department(form.name.data or "")
                    flash("Department created.", "success")
                    return redirect(url_for("school.department_list"))
                except ValidationError as exc:
                    for msg in exc.messages:
                        form.name.errors.append(msg)
            return render_template(
                template,
                departments=departments,
                create_form=form,
                edit_form=DepartmentForm(prefix="dept_edit"),
                show_create_modal=True,
                show_edit_modal=False,
            )

        if action == "update":
            try:
                pk = int(request.form.get("department_id", ""))
            except (TypeError, ValueError):
                flash("Invalid department.", "error")
                return redirect(url_for("school.department_list"))
            dept = dept_svc.get_department(pk)
            if dept is None:
                flash("Department not found.", "error")
                return redirect(url_for("school.department_list"))
            form = DepartmentForm(formdata=request.form, prefix="dept_edit")
            if form.validate():
                try:
                    dept_svc.update_department(pk, form.name.data or "")
                    flash("Department updated.", "success")
                    return redirect(url_for("school.department_list"))
                except ValidationError as exc:
                    for msg in exc.messages:
                        form.name.errors.append(msg)
            return render_template(
                template,
                departments=DepartmentService().list_departments(),
                create_form=DepartmentForm(prefix="dept_create"),
                edit_form=form,
                edit_department_id=pk,
                show_create_modal=False,
                show_edit_modal=True,
            )

        if action == "delete":
            try:
                pk = int(request.form.get("department_id", ""))
            except (TypeError, ValueError):
                flash("Invalid department.", "error")
                return redirect(url_for("school.department_list"))
            try:
                dept_svc.delete_department(pk)
                flash("Department deleted.", "success")
            except ValidationError as exc:
                flash(exc.messages[0] if exc.messages else str(exc), "error")
            return redirect(url_for("school.department_list"))

        return redirect(url_for("school.department_list"))

    return render_template(
        template,
        departments=departments,
        create_form=DepartmentForm(prefix="dept_create"),
        edit_form=DepartmentForm(prefix="dept_edit"),
        show_create_modal=False,
        show_edit_modal=False,
    )


@bp.route("/students", methods=["GET", "POST"], strict_slashes=False)
def student_list():
    template = "school/student_list.html"
    st_svc = StudentService()
    dept_svc = DepartmentService()
    all_departments = dept_svc.list_departments()
    students = st_svc.list_students()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            form = StudentForm(formdata=request.form, prefix="stu_create")
            form.apply_department_choices(all_departments)
            if form.validate():
                try:
                    st_svc.create_student(
                        student_number=form.student_number.data or "",
                        first_name=form.first_name.data or "",
                        last_name=form.last_name.data or "",
                        birth_date=form.birth_date.data,
                        department_id=form.department.data,
                    )
                    flash("Student created.", "success")
                    return redirect(url_for("school.student_list"))
                except ValidationError as exc:
                    for msg in exc.messages:
                        flash(msg, "error")
            return render_template(
                template,
                students=st_svc.list_students(),
                create_form=form,
                edit_form=_empty_student_form("stu_edit", all_departments),
                show_create_modal=True,
                show_edit_modal=False,
            )

        if action == "update":
            try:
                pk = int(request.form.get("student_id", ""))
            except (TypeError, ValueError):
                flash("Invalid student.", "error")
                return redirect(url_for("school.student_list"))
            student = st_svc.get_student(pk)
            if student is None:
                flash("Student not found.", "error")
                return redirect(url_for("school.student_list"))
            form = StudentForm(
                formdata=request.form,
                prefix="stu_edit",
                obj=student,
            )
            form.apply_department_choices(dept_svc.list_departments())
            if form.validate():
                try:
                    st_svc.update_student(
                        pk,
                        student_number=form.student_number.data or "",
                        first_name=form.first_name.data or "",
                        last_name=form.last_name.data or "",
                        birth_date=form.birth_date.data,
                        department_id=form.department.data,
                    )
                    flash("Student updated.", "success")
                    return redirect(url_for("school.student_list"))
                except ValidationError as exc:
                    for msg in exc.messages:
                        flash(msg, "error")
            return render_template(
                template,
                students=StudentService().list_students(),
                create_form=_empty_student_form("stu_create", all_departments),
                edit_form=form,
                edit_student_id=pk,
                show_create_modal=False,
                show_edit_modal=True,
            )

        if action == "delete":
            try:
                pk = int(request.form.get("student_id", ""))
            except (TypeError, ValueError):
                flash("Invalid student.", "error")
                return redirect(url_for("school.student_list"))
            try:
                st_svc.delete_student(pk)
                flash("Student deleted.", "success")
            except ValidationError as exc:
                flash(exc.messages[0] if exc.messages else str(exc), "error")
            return redirect(url_for("school.student_list"))

        return redirect(url_for("school.student_list"))

    create = StudentForm(prefix="stu_create")
    edit = StudentForm(prefix="stu_edit")
    create.apply_department_choices(all_departments)
    edit.apply_department_choices(all_departments)
    return render_template(
        template,
        students=students,
        create_form=create,
        edit_form=edit,
        show_create_modal=False,
        show_edit_modal=False,
    )


def _empty_student_form(prefix: str, departments) -> StudentForm:
    f = StudentForm(prefix=prefix)
    f.apply_department_choices(departments)
    return f
