"""
UAT (User Acceptance Test) otomasyonu: iş senaryoları adlarıyla tam akış.
Manuel UAT listesi için aynı senaryolar README veya ekip checklist'i ile eşleştirilebilir.

Çalıştırma: pytest -m uat
"""

import subprocess
import sys
from unittest.mock import patch

import pytest

import main as calc_main


@pytest.mark.uat
def test_uat_scenario_toplama_ve_cikis(capsys):
    """Senaryo: Kullanıcı toplama yapar ve menüden çıkar."""
    with patch("builtins.input", side_effect=["1", "10", "20", "5"]):
        calc_main.main()
    out = capsys.readouterr().out
    assert "10+20=30" in out.replace(" ", "")
    assert "Programdan çıkılıyor" in out


@pytest.mark.uat
def test_uat_scenario_carpma_subprocess(main_py):
    """Senaryo: Süreç dışından çarpma işlemi başarılı."""
    completed = subprocess.run(
        [sys.executable, str(main_py)],
        input="3\n4\n5\n5\n",
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=10,
    )
    assert completed.returncode == 0
    assert "4*5=20" in completed.stdout.replace(" ", "")


@pytest.mark.uat
def test_uat_scenario_sifira_bolme_uyarisi(capsys):
    """Senaryo: Sıfıra bölmede uyarı, uygulama çökmez, çıkış."""
    with patch("builtins.input", side_effect=["4", "1", "0", "5"]):
        calc_main.main()
    out = capsys.readouterr().out
    assert "Sıfıra bölme hatası" in out
