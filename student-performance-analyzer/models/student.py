# models/student.py — Student data model

class Student:
    def __init__(self, student_id=None, student_code=None, first_name=None,
                 last_name=None, email=None, created_at=None):
        self.student_id = student_id
        self.student_code = student_code
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = created_at

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def calculate_average(self, scores_list):
        """Return average percentage from a list of numeric scores."""
        if not scores_list:
            return 0.0
        return sum(scores_list) / len(scores_list)

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'student_code': self.student_code,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at,
        }

    def __str__(self):
        return f"{self.student_code} - {self.full_name}"
