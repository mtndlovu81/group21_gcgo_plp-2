# models/assessment.py — Assessment data model

class Assessment:
    def __init__(self, assessment_id=None, subject_id=None,
                 assessment_name=None, max_score=100, date_given=None):
        self.assessment_id = assessment_id
        self.subject_id = subject_id
        self.assessment_name = assessment_name
        self.max_score = max_score
        self.date_given = date_given

    def to_dict(self):
        return {
            'assessment_id': self.assessment_id,
            'subject_id': self.subject_id,
            'assessment_name': self.assessment_name,
            'max_score': self.max_score,
            'date_given': self.date_given,
        }

    def __str__(self):
        return f"{self.assessment_name} (max: {self.max_score})"
