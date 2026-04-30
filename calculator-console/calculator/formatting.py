def format_for_display(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)
