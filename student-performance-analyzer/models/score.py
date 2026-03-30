# models/score.py — Score data model

class Score:
    def __init__(self, score_id=None, student_id=None, assessment_id=None,
                 score_value=None, topic_id=None, recorded_at=None):
        self.score_id = score_id
        self.student_id = student_id
        self.assessment_id = assessment_id
        self.score_value = score_value
        self.topic_id = topic_id
        self.recorded_at = recorded_at

    def percentage(self, max_score):
        """Return score as a percentage of max_score."""
        if not max_score or max_score == 0:
            return 0.0
        return (self.score_value / max_score) * 100

    @staticmethod
    def get_performance_level(percentage):
        """Return performance label for a given percentage."""
        if percentage >= 80:
            return "Excellent"
        elif percentage >= 60:
            return "Good"
        elif percentage >= 40:
            return "Average"
        else:
            return "Needs Improvement"

    def to_dict(self):
        return {
            'score_id': self.score_id,
            'student_id': self.student_id,
            'assessment_id': self.assessment_id,
            'score_value': self.score_value,
            'topic_id': self.topic_id,
            'recorded_at': self.recorded_at,
        }

    def __str__(self):
        return f"Score({self.score_value})"
