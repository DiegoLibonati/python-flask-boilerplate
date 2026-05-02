from typing import Any


def is_positive_integer(value: Any) -> bool:
    try:
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return value > 0
        if isinstance(value, str) and value.isdigit():
            return int(value) > 0
        return False
    except Exception:
        return False
