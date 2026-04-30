"""Entegrasyon testleri: main döngüsü + mock stdin (bir kat üst, daha az sayıda)."""

from unittest.mock import patch

import pytest

import main as calc_main


@pytest.mark.integration
def test_add_then_exit(capsys):
    """Menü → toplama → iki sayı → sonuç → çıkış akışı."""
    user_lines = ["1", "2", "3", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    captured = capsys.readouterr().out
    assert "Sonuç:" in captured
    assert "2+3=5" in captured.replace(" ", "")
    assert "Programdan çıkılıyor" in captured


@pytest.mark.integration
def test_divide_by_zero_shows_error_then_continue_and_exit(capsys):
    """Bölme sıfır → hata mesajı; ikinci tur çıkış."""
    user_lines = [
        "4",  # bölme
        "10",
        "0",  # sıfıra bölme
        "5",  # çıkış
    ]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert "Sıfıra bölme hatası" in out
    assert "Programdan çıkılıyor" in out


@pytest.mark.integration
def test_invalid_menu_choice_reprompts(capsys):
    """Geçersiz menü seçimi sonrası yeniden sorulur, sonra geçerli seçim."""
    user_lines = ["9", "1", "1", "1", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert "Geçersiz seçim" in out
    assert "1+1=2" in out.replace(" ", "")


@pytest.mark.integration
def test_subtract_then_exit(capsys):
    user_lines = ["2", "10", "4", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert "10-4=6" in out.replace(" ", "")


@pytest.mark.integration
def test_multiply_then_exit(capsys):
    user_lines = ["3", "4", "5", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert "4*5=20" in out.replace(" ", "")


@pytest.mark.integration
def test_divide_success_then_exit(capsys):
    user_lines = ["4", "10", "2", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert "10/2=5" in out.replace(" ", "")


@pytest.mark.integration
def test_get_number_retries_on_empty_then_valid(capsys):
    """Boş satır → uyarı, geçerli sayıya kadar tekrar."""
    user_lines = ["1", "", "7", "8", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert "Hatalı giriş" in out
    assert "7+8=15" in out.replace(" ", "")


@pytest.mark.integration
def test_get_number_retries_on_non_numeric_then_valid(capsys):
    """float dışı metin → ValueError dalı, sonra geçerli sayı."""
    user_lines = ["1", "not-a-number", "3", "4", "5"]
    with patch("builtins.input", side_effect=user_lines):
        calc_main.main()
    out = capsys.readouterr().out
    assert out.count("Hatalı giriş") >= 1
    assert "3+4=7" in out.replace(" ", "")
