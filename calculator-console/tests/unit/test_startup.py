"""Birim testleri: modül yükleme sırasındaki stdout yapılandırması (izole import)."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

_MAIN_PATH = Path(__file__).resolve().parents[2] / "main.py"


def _load_main_fresh():
    """Paket önbelleğine yazmadan main.py yükle (reload yan etkisi olmadan)."""
    spec = importlib.util.spec_from_file_location("_calc_main_under_test", _MAIN_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.unit
def test_module_load_succeeds_when_stdout_reconfigure_raises_oserror():
    class StubStdout:
        def reconfigure(self, **_kwargs):
            raise OSError("no tty")

    with patch("sys.stdout", StubStdout()):
        mod = _load_main_fresh()
    assert mod.add(1, 1) == 2


@pytest.mark.unit
def test_module_load_succeeds_when_stdout_reconfigure_raises_valueerror():
    class StubStdout:
        def reconfigure(self, **_kwargs):
            raise ValueError("bad encoding")

    with patch("sys.stdout", StubStdout()):
        mod = _load_main_fresh()
    assert mod.subtract(2, 1) == 1


@pytest.mark.unit
def test_module_load_skips_reconfigure_when_stdout_has_no_reconfigure():
    out = SimpleNamespace(write=lambda *a, **k: None, flush=lambda: None)
    with patch("sys.stdout", out):
        mod = _load_main_fresh()
    assert mod.multiply(2, 3) == 6
