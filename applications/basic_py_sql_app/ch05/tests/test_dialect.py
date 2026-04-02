from db.backend_kind import DbBackend
from db.dialect import MysqlDialect, PostgresDialect, get_dialect


def test_get_dialect_postgres():
    d = get_dialect(DbBackend.POSTGRESQL)
    assert isinstance(d, PostgresDialect)


def test_get_dialect_mysql():
    d = get_dialect(DbBackend.MYSQL)
    assert isinstance(d, MysqlDialect)


def test_mysql_seed_sql_structure():
    sql = MysqlDialect().seed_students_sql()
    assert "INSERT IGNORE INTO students" in sql
    assert "UNION ALL" in sql
    assert "seed_rows" in sql
    assert "LIMIT 1" in sql


def test_postgres_conflict_syntax():
    sql = PostgresDialect().insert_student_ignore_sql()
    assert "ON CONFLICT" in sql
