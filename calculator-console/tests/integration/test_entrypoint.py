"""main.py dosyasının __main__ olarak çalışması (satır kapsamı)."""

import runpy
from pathlib import Path
from unittest.mock import patch

import pytest

_MAIN = Path(__file__).resolve().parents[2] / "main.py"


@pytest.mark.integration
def test_run_path_as_main_executes_main_and_exits(capsys):
    with patch("builtins.input", side_effect=["5"]):
        runpy.run_path(str(_MAIN), run_name="__main__")
    out = capsys.readouterr().out
    assert "Programdan çıkılıyor" in out
