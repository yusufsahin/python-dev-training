import pytest
from calculator.validation import validate_calculator_input

@pytest.mark.unit
def test_validation_success():
    data = {"operation": "add", "first_number": "10", "second_number": "5"}
    is_valid, errors, validated = validate_calculator_input(data)
    assert is_valid is True
    assert not errors
    assert validated["operation"] == "add"
    assert validated["first_number"] == 10.0
    assert validated["second_number"] == 5.0

@pytest.mark.unit
def test_validation_missing_fields():
    data = {}
    is_valid, errors, validated = validate_calculator_input(data)
    assert is_valid is False
    assert "operation" in errors
    assert "first_number" in errors
    assert "second_number" in errors

@pytest.mark.unit
def test_validation_invalid_numbers():
    data = {"operation": "multiply", "first_number": "abc", "second_number": "def"}
    is_valid, errors, validated = validate_calculator_input(data)
    assert is_valid is False
    assert "first_number" in errors
    assert "second_number" in errors

@pytest.mark.unit
def test_validation_divide_by_zero():
    data = {"operation": "divide", "first_number": "10", "second_number": "0"}
    is_valid, errors, validated = validate_calculator_input(data)
    assert is_valid is False
    assert "second_number" in errors
    assert "Sıfıra bölme" in errors["second_number"]

@pytest.mark.unit
def test_validation_invalid_operation():
    data = {"operation": "modulo", "first_number": "10", "second_number": "5"}
    is_valid, errors, validated = validate_calculator_input(data)
    assert is_valid is False
    assert "operation" in errors
