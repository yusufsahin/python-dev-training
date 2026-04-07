from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for

from tasks.exceptions import ValidationError
from tasks.forms import TaskForm
from tasks.services import TaskService

bp = Blueprint("tasks", __name__)


def _status_display(status: str) -> str:
    return {
        "todo": "Todo",
        "in_progress": "In progress",
        "done": "Done",
    }.get(status, status)


@bp.route("/")
def home():
    svc = TaskService()
    return render_template(
        "tasks/home.html",
        task_count=len(svc.list_tasks()),
    )


@bp.route("/tasks", methods=["GET", "POST"], strict_slashes=False)
def task_list():
    template = "tasks/task_list.html"
    svc = TaskService()
    tasks = svc.list_tasks()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "create":
            form = TaskForm(formdata=request.form, prefix="task_create")
            if form.validate():
                try:
                    svc.create_task(
                        title=form.title.data or "",
                        status=form.status.data,
                        start_date=form.start_date.data,
                        end_date=form.end_date.data,
                    )
                    flash("Task created.", "success")
                    return redirect(url_for("tasks.task_list"))
                except ValidationError as exc:
                    for msg in exc.messages:
                        flash(msg, "error")
            return render_template(
                template,
                tasks=svc.list_tasks(),
                create_form=form,
                edit_form=TaskForm(prefix="task_edit"),
                show_create_modal=True,
                show_edit_modal=False,
                status_display=_status_display,
            )

        if action == "update":
            pk = (request.form.get("task_id") or "").strip()
            if not pk:
                flash("Invalid task.", "error")
                return redirect(url_for("tasks.task_list"))
            task = svc.get_task(pk)
            if task is None:
                flash("Task not found.", "error")
                return redirect(url_for("tasks.task_list"))
            form = TaskForm(formdata=request.form, prefix="task_edit")
            if form.validate():
                try:
                    svc.update_task(
                        pk,
                        title=form.title.data or "",
                        status=form.status.data,
                        start_date=form.start_date.data,
                        end_date=form.end_date.data,
                    )
                    flash("Task updated.", "success")
                    return redirect(url_for("tasks.task_list"))
                except ValidationError as exc:
                    for msg in exc.messages:
                        flash(msg, "error")
            return render_template(
                template,
                tasks=TaskService().list_tasks(),
                create_form=TaskForm(prefix="task_create"),
                edit_form=form,
                edit_task_id=pk,
                show_create_modal=False,
                show_edit_modal=True,
                status_display=_status_display,
            )

        if action == "delete":
            pk = (request.form.get("task_id") or "").strip()
            if not pk:
                flash("Invalid task.", "error")
                return redirect(url_for("tasks.task_list"))
            try:
                svc.delete_task(pk)
                flash("Task deleted.", "success")
            except ValidationError as exc:
                flash(exc.messages[0] if exc.messages else str(exc), "error")
            return redirect(url_for("tasks.task_list"))

        return redirect(url_for("tasks.task_list"))

    return render_template(
        template,
        tasks=tasks,
        create_form=TaskForm(prefix="task_create"),
        edit_form=TaskForm(prefix="task_edit"),
        show_create_modal=False,
        show_edit_modal=False,
        status_display=_status_display,
    )
