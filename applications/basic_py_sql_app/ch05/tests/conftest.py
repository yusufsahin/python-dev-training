import threading
from http.server import HTTPServer
from unittest.mock import MagicMock

import pytest

import web.api as api_module
from web.handlers import StudentAppHandler


@pytest.fixture
def mock_student_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_department_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def api_server(mock_student_service, mock_department_service, monkeypatch):
    monkeypatch.setattr(api_module, "student_service", mock_student_service)
    monkeypatch.setattr(api_module, "department_service", mock_department_service)
    httpd = HTTPServer(("127.0.0.1", 0), StudentAppHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{port}"
    try:
        yield base, mock_student_service, mock_department_service
    finally:
        httpd.shutdown()
        httpd.server_close()
        thread.join(timeout=3)
