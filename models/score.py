class Score:
    def __init__(self, value):
        self.value = value

    def get_level(self):
        if self.value >= 80:
            return "Excellent"
        elif self.value >= 60:
            return "Good"
        elif self.value >= 40:
            return "Average"
        else:
            return "Needs Improvement"
