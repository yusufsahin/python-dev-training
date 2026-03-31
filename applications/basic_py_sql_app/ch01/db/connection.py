import psycopg

CONN_STR = "dbname=db_app01 user=postgres password=Aloha@2026 host=localhost port=5432"


def get_connection():
    return psycopg.connect(CONN_STR)
