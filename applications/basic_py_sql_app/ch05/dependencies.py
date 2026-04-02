"""Uygulama genelinde tek bir ConnectionFactory ve SQL lehçesi ile servis örnekleri."""

from db.backend_kind import DbBackend
from db.config import load_db_context
from db.dialect import SqlDialect, get_dialect
from ports import ConnectionFactory
from repositories.department_repository import SqlDepartmentRepository
from repositories.student_repository import SqlStudentRepository
from services.department_service import DepartmentService
from services.student_service import StudentService


def build_services(
    connect: ConnectionFactory | None = None,
    backend: DbBackend | None = None,
    dialect: SqlDialect | None = None,
) -> tuple[StudentService, DepartmentService]:
    if connect is not None:
        resolved_backend = backend or DbBackend.POSTGRESQL
        factory = connect
        d = dialect or get_dialect(resolved_backend)
    else:
        ctx = load_db_context()
        factory = ctx.connect
        d = dialect or get_dialect(ctx.backend)

    student_repository = SqlStudentRepository(factory, d)
    department_repository = SqlDepartmentRepository(factory, d)
    return (
        StudentService(student_repository, factory, d),
        DepartmentService(department_repository),
    )


def configure_services(
    connect: ConnectionFactory | None = None,
    backend: DbBackend | None = None,
    dialect: SqlDialect | None = None,
) -> None:
    """Test veya özel bağlantı için servisleri yeniden kurar."""
    global student_service, department_service
    student_service, department_service = build_services(connect, backend, dialect)


student_service, department_service = build_services()
