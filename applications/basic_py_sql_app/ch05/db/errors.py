"""Sürücüden bağımsız bütünlük (unique / FK) hata kontrolü."""


def is_integrity_error(exc: BaseException) -> bool:
    try:
        import psycopg

        if isinstance(exc, psycopg.IntegrityError):
            return True
    except ImportError:
        pass
    try:
        import pymysql.err

        if isinstance(exc, pymysql.err.IntegrityError):
            return True
    except ImportError:
        pass
    return False
