"""app.py savunma katmanı ve __main__ giriş noktası kapsamı."""

import runpy
from pathlib import Path
from unittest.mock import MagicMock

import flask
import pytest

_APP_PATH = Path(__file__).resolve().parents[2] / "app.py"


@pytest.mark.web
def test_post_divide_sets_error_when_function_returns_none(client, monkeypatch):
    """
    Validasyon atlanırsa (ör. iletken savunma) divide(None) yolu — app satır 32-33.
    """
    import app as app_module

    def fake_validate(_form_data):
        return True, {}, {
            "operation": "divide",
            "first_number": 10.0,
            "second_number": 0.0,
        }

    monkeypatch.setattr(app_module, "validate_calculator_input", fake_validate)
    response = client.post(
        "/",
        data={
            "operation": "divide",
            "first_number": "10",
            "second_number": "0",
        },
    )
    assert response.status_code == 200
    assert "Sıfıra bölme hatası".encode("utf-8") in response.data


@pytest.mark.web
def test_app_py_main_calls_flask_run(monkeypatch):
    """python app.py → Flask.run(debug=True) — app satır 42-43."""
    mock_run = MagicMock()
    monkeypatch.setattr(flask.Flask, "run", mock_run)
    runpy.run_path(str(_APP_PATH), run_name="__main__")
    mock_run.assert_called_once()
    assert mock_run.call_args.kwargs.get("debug") is True
