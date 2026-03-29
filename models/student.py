class Student:
    def __init__(self, student_id, name, score):
        self.student_id = student_id
        self.name = name
        self.score = score

    def get_performance(self):
        if self.score >= 80:
            return "Excellent"
        elif self.score >= 60:
            return "Good"
        elif self.score >= 40:
            return "Average"
        else:
            return "Needs Improvement"

    def __str__(self):
        return "{} - {} ({})".format(self.student_id, self.name, self.score)
