import os
from http.server import ThreadingHTTPServer

from web.handlers import StudentAppHandler


def _try_initialize_database_schema() -> None:
    """DB ayaktaysa tabloları oluşturur; yoksa uyarı verir (manuel Create Tables kalır)."""
    if os.environ.get("SKIP_AUTO_DB_INIT", "").lower() in ("1", "true", "yes"):
        return
    try:
        from dependencies import student_service

        student_service.initialize_app()
        print("Database schema ready (create_table completed).")
    except Exception as exc:
        print(
            f"Note: Database not reachable at startup ({exc!s}). "
            "Start PostgreSQL/MySQL and use Create Tables, or fix POSTGRES_DSN / MYSQL_*."
        )


def run_server(host: str | None = None, port: int | None = None) -> None:
    host = host if host is not None else os.environ.get("HOST", "127.0.0.1")
    port = int(port if port is not None else os.environ.get("PORT", "8000"))
    _try_initialize_database_schema()
    server = ThreadingHTTPServer((host, port), StudentAppHandler)
    print(f"Server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
