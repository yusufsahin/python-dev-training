from typing import Literal

import psycopg

from db.connection import get_connection
from dto.department_dto import DepartmentCreate, DepartmentUpdate
from models.department import Department


def list_departments() -> list[Department]:
    sql = "SELECT id, name FROM departments ORDER BY id;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            return [Department(id=row[0], name=row[1]) for row in rows]


def insert_department(department: DepartmentCreate) -> bool:
    sql = """
        INSERT INTO departments (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (department.name,))
            conn.commit()
            return cur.rowcount > 0


def get_department_by_id(department_id: int) -> Department | None:
    sql = "SELECT id, name FROM departments WHERE id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (department_id,))
            row = cur.fetchone()
            if row is None:
                return None

            return Department(id=row[0], name=row[1])


def update_department(
    department_id: int, department: DepartmentUpdate
) -> Literal["updated", "not_found", "conflict"]:
    sql = "UPDATE departments SET name = %s WHERE id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, (department.name, department_id))
                conn.commit()
            except psycopg.IntegrityError:
                conn.rollback()
                return "conflict"

            if cur.rowcount == 0:
                return "not_found"

            return "updated"


def delete_department(department_id: int) -> Literal["deleted", "not_found", "in_use"]:
    sql = "DELETE FROM departments WHERE id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, (department_id,))
                conn.commit()
            except psycopg.IntegrityError:
                conn.rollback()
                return "in_use"

            if cur.rowcount == 0:
                return "not_found"

            return "deleted"


def department_exists(department_id: int) -> bool:
    sql = "SELECT 1 FROM departments WHERE id = %s;"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (department_id,))
            return cur.fetchone() is not None
