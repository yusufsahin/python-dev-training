from db.config import load_db_context
from db.dialect import MysqlDialect, SqlDialect, get_dialect
from ports import ConnectionFactory


def seed_data(
    connect: ConnectionFactory | None = None, dialect: SqlDialect | None = None
) -> int:
    if connect is None or dialect is None:
        ctx = load_db_context()
        factory = connect or ctx.connect
        d = dialect or get_dialect(ctx.backend)
    else:
        factory = connect
        d = dialect

    with factory() as conn:
        with conn.cursor() as cur:
            cur.execute(d.seed_extra_departments_sql())
            cur.execute(d.seed_students_sql())
            # MySQL: çok satırlı INSERT…SELECT sonrası driver rowcount güvenilmez olabiliyor
            if isinstance(d, MysqlDialect):
                cur.execute("SELECT ROW_COUNT()")
                row = cur.fetchone()
                inserted_count = int(row[0]) if row and row[0] is not None else 0
            else:
                inserted_count = cur.rowcount
            conn.commit()
            return inserted_count
