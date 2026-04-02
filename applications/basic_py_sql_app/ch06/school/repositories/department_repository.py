from school.models import Department


class DjangoDepartmentRepository:
    def list_all(self) -> list[Department]:
        return list(Department.objects.order_by("id"))

    def get_by_id(self, department_id: int) -> Department | None:
        try:
            return Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return None

    def create(self, name: str) -> Department:
        return Department.objects.create(name=name)

    def update(self, department: Department, name: str) -> Department:
        department.name = name
        department.save(update_fields=["name"])
        return department

    def delete(self, department: Department) -> None:
        department.delete()

    def name_exists(self, name: str, exclude_pk: int | None = None) -> bool:
        qs = Department.objects.filter(name=name)
        if exclude_pk is not None:
            qs = qs.exclude(pk=exclude_pk)
        return qs.exists()
