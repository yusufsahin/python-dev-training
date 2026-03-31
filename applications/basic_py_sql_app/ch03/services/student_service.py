from db.schema import create_table
from db.seed import seed_data
from repositories.student_repository import (
    delete_student,
    get_student_by_id,
    insert_student,
    list_students,
    update_student,
)


def initialize_app():
    create_table()


def load_seed_data():
    return seed_data()


def get_students():
    return list_students()


def get_student(student_id):
    return get_student_by_id(student_id)


def add_student(student_number, first_name, last_name, birth_date, department_id):
    return insert_student(student_number, first_name, last_name, birth_date, department_id)


def edit_student(student_id, student_number, first_name, last_name, birth_date, department_id):
    return update_student(student_id, student_number, first_name, last_name, birth_date, department_id)


def remove_student(student_id):
    return delete_student(student_id)
