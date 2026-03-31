from repositories.department_repository import (
    department_exists,
    insert_department,
    list_departments,
)


def get_departments():
    return list_departments()


def add_department(name):
    return insert_department(name)


def is_valid_department(department_id):
    return department_exists(department_id)
