from typing import Dict, Optional, Tuple, Any

SUPPORTED_OPERATIONS = {"add", "subtract", "multiply", "divide"}

def validate_calculator_input(form_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str], Dict[str, Any]]:
    errors = {}
    validated_data = {}

    operation = form_data.get("operation")
    if not operation:
        errors["operation"] = "Lütfen bir işlem seçiniz."
    elif operation not in SUPPORTED_OPERATIONS:
        errors["operation"] = "Geçersiz işlem seçildi."
    else:
        validated_data["operation"] = operation

    first_number_raw = form_data.get("first_number", "").strip()
    if not first_number_raw:
        errors["first_number"] = "Lütfen birinci sayıyı giriniz."
    else:
        try:
            validated_data["first_number"] = float(first_number_raw)
        except ValueError:
            errors["first_number"] = "Hatalı giriş. Lütfen geçerli bir sayı giriniz."

    second_number_raw = form_data.get("second_number", "").strip()
    if not second_number_raw:
        errors["second_number"] = "Lütfen ikinci sayıyı giriniz."
    else:
        try:
            val = float(second_number_raw)
            validated_data["second_number"] = val
            if operation == "divide" and val == 0:
                errors["second_number"] = "Sıfıra bölme hatası. İkinci sayı 0 olamaz."
        except ValueError:
            errors["second_number"] = "Hatalı giriş. Lütfen geçerli bir sayı giriniz."

    return len(errors) == 0, errors, validated_data
