"""Birim testleri: saf matematik işlemleri (piramidin tabanı, en çok sayıda)."""

import pytest

from calculator.operations import add, divide, multiply, subtract


@pytest.mark.unit
def test_add_positive_and_negative():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


@pytest.mark.unit
def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(0, 5) == -5


@pytest.mark.unit
def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10


@pytest.mark.unit
def test_divide_normal():
    assert divide(10, 2) == 5.0
    assert divide(1, 3) == pytest.approx(1 / 3)


@pytest.mark.unit
def test_divide_by_zero_returns_none():
    assert divide(5, 0) is None


@pytest.mark.unit
def test_add_float_precision():
    assert add(0.1, 0.2) == pytest.approx(0.3)


@pytest.mark.unit
def test_divide_negative_operands():
    assert divide(-12, 3) == -4.0
    assert divide(9, -3) == -3.0


@pytest.mark.unit
def test_multiply_by_zero():
    assert multiply(0, 99) == 0


@pytest.mark.unit
def test_subtract_floats():
    assert subtract(0.5, 0.25) == pytest.approx(0.25)
