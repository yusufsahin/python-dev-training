from services.department_service import add_department, get_departments
from services.student_service import initialize_app, load_seed_data


def handle_initialize_app():
    initialize_app()
    return "Table ready."


def handle_add_department(department_name):
    if add_department(department_name):
        return "Department inserted."

    return "Department already exists."


def handle_list_departments():
    return get_departments()


def handle_seed_data():
    inserted_count = load_seed_data()
    return f"Seed data inserted. Added {inserted_count} students."
