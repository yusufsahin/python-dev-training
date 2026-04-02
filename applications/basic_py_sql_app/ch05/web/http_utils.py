from datetime import datetime


def parse_birth_date(value: str):
    return datetime.strptime(value, "%Y-%m-%d").date()


def db_error_message(exc: BaseException) -> str:
    try:
        import psycopg.errors

        if isinstance(exc, psycopg.errors.UndefinedTable):
            return "Tables are missing. Use Create Tables on the home page."
    except ImportError:
        pass
    try:
        import pymysql.err

        if isinstance(exc, pymysql.err.ProgrammingError) and exc.args and exc.args[0] == 1146:
            return "Tables are missing. Use Create Tables on the home page."
    except ImportError:
        pass
    text = str(exc).lower()
    if (
        "connection refused" in text
        or "could not connect" in text
        or "name or service not known" in text
        or "timed out" in text
    ):
        return (
            "Cannot connect to the database. Ensure PostgreSQL/MySQL is running and "
            "DB_BACKEND, POSTGRES_DSN or MYSQL_* match your setup (Docker: host=db)."
        )
    return "Database is not ready yet. Use Create Tables first."
