from typing import Literal

from db.config import load_db_context
from db.dialect import SqlDialect, get_dialect
from db.errors import is_integrity_error
from dto.department_dto import DepartmentCreate, DepartmentUpdate
from models.department import Department
from ports import ConnectionFactory


class SqlDepartmentRepository:
    def __init__(
        self,
        connect: ConnectionFactory | None = None,
        dialect: SqlDialect | None = None,
    ) -> None:
        if connect is None or dialect is None:
            ctx = load_db_context()
            self._connect = connect or ctx.connect
            self._dialect = dialect or get_dialect(ctx.backend)
        else:
            self._connect = connect
            self._dialect = dialect

    def list_departments(self) -> list[Department]:
        sql = "SELECT id, name FROM departments ORDER BY id;"

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return [Department(id=row[0], name=row[1]) for row in rows]

    def insert_department(self, department: DepartmentCreate) -> bool:
        sql = self._dialect.insert_department_ignore_sql()

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (department.name,))
                conn.commit()
                return cur.rowcount > 0

    def get_department_by_id(self, department_id: int) -> Department | None:
        sql = "SELECT id, name FROM departments WHERE id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (department_id,))
                row = cur.fetchone()
                if row is None:
                    return None

                return Department(id=row[0], name=row[1])

    def update_department(
        self, department_id: int, department: DepartmentUpdate
    ) -> Literal["updated", "not_found", "conflict"]:
        sql = "UPDATE departments SET name = %s WHERE id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(sql, (department.name, department_id))
                    conn.commit()
                except Exception as exc:
                    if is_integrity_error(exc):
                        conn.rollback()
                        return "conflict"
                    raise

                if cur.rowcount == 0:
                    return "not_found"

                return "updated"

    def delete_department(
        self, department_id: int
    ) -> Literal["deleted", "not_found", "in_use"]:
        sql = "DELETE FROM departments WHERE id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(sql, (department_id,))
                    conn.commit()
                except Exception as exc:
                    if is_integrity_error(exc):
                        conn.rollback()
                        return "in_use"
                    raise

                if cur.rowcount == 0:
                    return "not_found"

                return "deleted"

    def department_exists(self, department_id: int) -> bool:
        sql = "SELECT 1 FROM departments WHERE id = %s;"

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (department_id,))
                return cur.fetchone() is not None
