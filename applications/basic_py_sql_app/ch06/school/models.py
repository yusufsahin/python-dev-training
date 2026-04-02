from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    student_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.student_number} ({self.first_name} {self.last_name})"
