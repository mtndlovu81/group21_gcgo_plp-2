# models/subject.py — Subject data model

class Subject:
    def __init__(self, subject_id=None, subject_name=None):
        self.subject_id = subject_id
        self.subject_name = subject_name

    def to_dict(self):
        return {
            'subject_id': self.subject_id,
            'subject_name': self.subject_name,
        }

    def __str__(self):
        return f"{self.subject_name}"
