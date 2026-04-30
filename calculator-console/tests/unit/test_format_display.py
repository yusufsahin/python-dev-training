"""Birim testleri: sonuç gösterim formatı."""

import pytest

from calculator.formatting import format_for_display


@pytest.mark.unit
def test_format_integer_like_float_as_int_string():
    assert format_for_display(4.0) == "4"
    assert format_for_display(-0.0) == "0"


@pytest.mark.unit
def test_format_true_float():
    assert format_for_display(1.5) == "1.5"
    assert format_for_display(2.333) == "2.333"


@pytest.mark.unit
def test_format_large_integer_like():
    assert format_for_display(1_000_000.0) == "1000000"


@pytest.mark.unit
def test_format_non_whole_float_uses_str_repr():
    """Tam sayıya eşit olmayan değerler str(value) ile döner."""
    assert format_for_display(1e-7) == str(1e-7)
