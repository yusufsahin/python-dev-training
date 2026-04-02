from django.urls import path

from school import views

app_name = "school"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path("students/", views.StudentListView.as_view(), name="student_list"),
]
