"""Sistem testleri: gerçek Python süreci, gerçek stdin/stdout (az sayıda, yavaş olabilir)."""

import subprocess
import sys

import pytest


@pytest.mark.system
def test_subprocess_add_and_exit(main_py):
    completed = subprocess.run(
        [sys.executable, str(main_py)],
        input="1\n2\n3\n5\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
    )
    assert completed.returncode == 0
    assert "Sonuç:" in completed.stdout
    assert "2+3=5" in completed.stdout.replace(" ", "")


@pytest.mark.system
def test_subprocess_immediate_exit(main_py):
    completed = subprocess.run(
        [sys.executable, str(main_py)],
        input="5\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
    )
    assert completed.returncode == 0
    assert "Programdan çıkılıyor" in completed.stdout
