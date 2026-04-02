from school.models import Department, Student


class DjangoStudentRepository:
    def list_all(self) -> list[Student]:
        return list(
            Student.objects.select_related("department").order_by("id"),
        )

    def get_by_id(self, student_id: int) -> Student | None:
        try:
            return Student.objects.select_related("department").get(pk=student_id)
        except Student.DoesNotExist:
            return None

    def create(
        self,
        *,
        student_number: str,
        first_name: str,
        last_name: str,
        birth_date,
        department_id: int,
    ) -> Student:
        dept = Department.objects.get(pk=department_id)
        return Student.objects.create(
            student_number=student_number,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            department=dept,
        )

    def update(
        self,
        student: Student,
        *,
        student_number: str,
        first_name: str,
        last_name: str,
        birth_date,
        department_id: int,
    ) -> Student:
        dept = Department.objects.get(pk=department_id)
        student.student_number = student_number
        student.first_name = first_name
        student.last_name = last_name
        student.birth_date = birth_date
        student.department = dept
        student.save()
        return student

    def delete(self, student: Student) -> None:
        student.delete()

    def department_exists(self, department_id: int) -> bool:
        return Department.objects.filter(pk=department_id).exists()

    def student_number_exists(self, student_number: str, exclude_pk: int | None = None) -> bool:
        qs = Student.objects.filter(student_number=student_number)
        if exclude_pk is not None:
            qs = qs.exclude(pk=exclude_pk)
        return qs.exists()
