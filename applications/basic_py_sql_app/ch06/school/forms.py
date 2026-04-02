from django import forms

from school.models import Department, Student


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Department name",
                    "autocomplete": "organization",
                }
            ),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_number",
            "first_name",
            "last_name",
            "birth_date",
            "department",
        ]
        widgets = {
            "student_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. 2024001"}
            ),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "department": forms.Select(attrs={"class": "form-select"}),
        }
