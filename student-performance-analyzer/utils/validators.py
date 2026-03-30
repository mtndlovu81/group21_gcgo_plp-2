import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_student_code(code):
    pattern = r'^S\d{4}$'  # e.g., S1234
    return bool(re.match(pattern, code))

def validate_score(score):
    return 0 <= score <= 100

def validate_non_empty(value):
    return bool(value.strip())
