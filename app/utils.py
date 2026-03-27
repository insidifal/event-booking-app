import re

def is_safe_string(string: str):
    safe_pattern = r"^[A-Za-z0-9_!@#$.-]+$"
    check = re.fullmatch(safe_pattern, string)
    return check is not None
