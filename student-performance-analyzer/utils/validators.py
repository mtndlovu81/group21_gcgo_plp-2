# utils/validators.py — Input validation helpers
# All functions return (is_valid: bool, error_message: str)

import re


def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if email and re.match(pattern, str(email)):
        return True, ""
    return False, "Invalid email format (e.g. user@example.com)"


def validate_student_code(code):
    # Expected format: ALU-2026-001  (letters - 4 digits - 3+ digits)
    pattern = r'^[A-Z]+-\d{4}-\d{3,}$'
    if code and re.match(pattern, str(code)):
        return True, ""
    return False, "Student code must follow format: ALU-2026-001"


def validate_score(value, max_score=100):
    try:
        value = float(value)
        max_score = float(max_score)
    except (TypeError, ValueError):
        return False, "Score must be a number"
    if 0 <= value <= max_score:
        return True, ""
    return False, f"Score must be between 0 and {max_score}"


def validate_non_empty(value, field_name="Field"):
    if value and str(value).strip():
        return True, ""
    return False, f"{field_name} cannot be empty"


def validate_menu_choice(choice, max_option):
    try:
        n = int(choice)
        if 1 <= n <= max_option:
            return True, ""
        return False, f"Please enter a number between 1 and {max_option}"
    except (TypeError, ValueError):
        return False, "Please enter a valid number"
