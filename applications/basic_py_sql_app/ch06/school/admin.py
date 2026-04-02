from django.contrib import admin

from school.models import Department, Student


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "student_number", "first_name", "last_name", "birth_date", "department")
    list_select_related = ("department",)
    search_fields = ("student_number", "first_name", "last_name")
    list_filter = ("department",)
