from datetime import date

import pytest

from web.http_utils import db_error_message, parse_birth_date


def test_parse_birth_date_valid():
    assert parse_birth_date("2010-12-31") == date(2010, 12, 31)


def test_parse_birth_date_invalid():
    with pytest.raises(ValueError):
        parse_birth_date("not-a-date")


def test_db_error_message_connection_refused():
    msg = db_error_message(Exception("connection refused"))
    assert "connect" in msg.lower()


def test_db_error_message_generic():
    msg = db_error_message(Exception("something else"))
    assert "Create Tables" in msg or "not ready" in msg.lower()
