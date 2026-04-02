from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from school.forms import DepartmentForm, StudentForm
from school.services import DepartmentService, StudentService


class HomeView(TemplateView):
    template_name = "school/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        dept_svc = DepartmentService()
        st_svc = StudentService()
        ctx["department_count"] = len(dept_svc.list_departments())
        ctx["student_count"] = len(st_svc.list_students())
        return ctx


class DepartmentListView(View):
    template_name = "school/department_list.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "departments": DepartmentService().list_departments(),
                "create_form": DepartmentForm(prefix="dept_create"),
                "edit_form": DepartmentForm(prefix="dept_edit"),
            },
        )

    def post(self, request):
        action = request.POST.get("action")
        dept_svc = DepartmentService()
        departments = dept_svc.list_departments()

        if action == "create":
            form = DepartmentForm(request.POST, prefix="dept_create")
            if form.is_valid():
                try:
                    dept_svc.create_department(form.cleaned_data["name"])
                    messages.success(request, "Department created.")
                    return redirect("school:department_list")
                except ValidationError as exc:
                    for msg in exc.messages:
                        form.add_error(None, msg)
            return render(
                request,
                self.template_name,
                {
                    "departments": departments,
                    "create_form": form,
                    "edit_form": DepartmentForm(prefix="dept_edit"),
                    "show_create_modal": True,
                },
            )

        if action == "update":
            try:
                pk = int(request.POST.get("department_id", ""))
            except (TypeError, ValueError):
                messages.error(request, "Invalid department.")
                return redirect("school:department_list")
            dept = dept_svc.get_department(pk)
            if dept is None:
                messages.error(request, "Department not found.")
                return redirect("school:department_list")
            form = DepartmentForm(request.POST, instance=dept, prefix="dept_edit")
            if form.is_valid():
                try:
                    dept_svc.update_department(pk, form.cleaned_data["name"])
                    messages.success(request, "Department updated.")
                    return redirect("school:department_list")
                except ValidationError as exc:
                    for msg in exc.messages:
                        form.add_error(None, msg)
            return render(
                request,
                self.template_name,
                {
                    "departments": DepartmentService().list_departments(),
                    "create_form": DepartmentForm(prefix="dept_create"),
                    "edit_form": form,
                    "edit_department_id": pk,
                    "show_edit_modal": True,
                },
            )

        if action == "delete":
            try:
                pk = int(request.POST.get("department_id", ""))
            except (TypeError, ValueError):
                messages.error(request, "Invalid department.")
                return redirect("school:department_list")
            try:
                dept_svc.delete_department(pk)
                messages.success(request, "Department deleted.")
            except ValidationError as exc:
                messages.error(
                    request, exc.messages[0] if exc.messages else str(exc)
                )
            return redirect("school:department_list")

        return redirect("school:department_list")


class StudentListView(View):
    template_name = "school/student_list.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "students": StudentService().list_students(),
                "create_form": StudentForm(prefix="stu_create"),
                "edit_form": StudentForm(prefix="stu_edit"),
            },
        )

    def post(self, request):
        action = request.POST.get("action")
        st_svc = StudentService()

        if action == "create":
            form = StudentForm(request.POST, prefix="stu_create")
            if form.is_valid():
                d = form.cleaned_data
                try:
                    st_svc.create_student(
                        student_number=d["student_number"],
                        first_name=d["first_name"],
                        last_name=d["last_name"],
                        birth_date=d["birth_date"],
                        department_id=d["department"].pk,
                    )
                    messages.success(request, "Student created.")
                    return redirect("school:student_list")
                except ValidationError as exc:
                    for msg in exc.messages:
                        form.add_error(None, msg)
            return render(
                request,
                self.template_name,
                {
                    "students": st_svc.list_students(),
                    "create_form": form,
                    "edit_form": StudentForm(prefix="stu_edit"),
                    "show_create_modal": True,
                },
            )

        if action == "update":
            try:
                pk = int(request.POST.get("student_id", ""))
            except (TypeError, ValueError):
                messages.error(request, "Invalid student.")
                return redirect("school:student_list")
            student = st_svc.get_student(pk)
            if student is None:
                messages.error(request, "Student not found.")
                return redirect("school:student_list")
            form = StudentForm(request.POST, instance=student, prefix="stu_edit")
            if form.is_valid():
                d = form.cleaned_data
                try:
                    st_svc.update_student(
                        pk,
                        student_number=d["student_number"],
                        first_name=d["first_name"],
                        last_name=d["last_name"],
                        birth_date=d["birth_date"],
                        department_id=d["department"].pk,
                    )
                    messages.success(request, "Student updated.")
                    return redirect("school:student_list")
                except ValidationError as exc:
                    for msg in exc.messages:
                        form.add_error(None, msg)
            return render(
                request,
                self.template_name,
                {
                    "students": StudentService().list_students(),
                    "create_form": StudentForm(prefix="stu_create"),
                    "edit_form": form,
                    "edit_student_id": pk,
                    "show_edit_modal": True,
                },
            )

        if action == "delete":
            try:
                pk = int(request.POST.get("student_id", ""))
            except (TypeError, ValueError):
                messages.error(request, "Invalid student.")
                return redirect("school:student_list")
            try:
                st_svc.delete_student(pk)
                messages.success(request, "Student deleted.")
            except ValidationError as exc:
                messages.error(
                    request, exc.messages[0] if exc.messages else str(exc)
                )
            return redirect("school:student_list")

        return redirect("school:student_list")
