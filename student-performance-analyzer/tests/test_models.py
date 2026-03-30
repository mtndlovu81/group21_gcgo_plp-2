# tests/test_models.py — Unit tests for model classes

import unittest
from models.student import Student
from models.subject import Subject
from models.assessment import Assessment
from models.score import Score


class TestScore(unittest.TestCase):

    def test_performance_level_boundaries(self):
        """Score.get_performance_level should return correct label at every boundary."""
        self.assertEqual(Score.get_performance_level(0),   'Needs Improvement')
        self.assertEqual(Score.get_performance_level(39),  'Needs Improvement')
        self.assertEqual(Score.get_performance_level(40),  'Average')
        self.assertEqual(Score.get_performance_level(59),  'Average')
        self.assertEqual(Score.get_performance_level(60),  'Good')
        self.assertEqual(Score.get_performance_level(79),  'Good')
        self.assertEqual(Score.get_performance_level(80),  'Excellent')
        self.assertEqual(Score.get_performance_level(100), 'Excellent')

    def test_percentage(self):
        sc = Score(score_value=75)
        self.assertAlmostEqual(sc.percentage(100), 75.0)
        self.assertAlmostEqual(sc.percentage(150), 50.0)

    def test_percentage_zero_max(self):
        sc = Score(score_value=50)
        self.assertEqual(sc.percentage(0), 0.0)

    def test_to_dict_keys(self):
        sc = Score(score_id=1, student_id=2, assessment_id=3, score_value=80)
        d  = sc.to_dict()
        for key in ['score_id', 'student_id', 'assessment_id', 'score_value', 'topic_id', 'recorded_at']:
            self.assertIn(key, d)

    def test_str(self):
        sc = Score(score_value=42)
        self.assertEqual(str(sc), 'Score(42)')


class TestStudent(unittest.TestCase):

    def test_full_name(self):
        s = Student(first_name='Jane', last_name='Doe')
        self.assertEqual(s.full_name, 'Jane Doe')

    def test_calculate_average(self):
        s = Student()
        self.assertAlmostEqual(s.calculate_average([80, 60, 40]), 60.0)

    def test_calculate_average_empty(self):
        s = Student()
        self.assertEqual(s.calculate_average([]), 0.0)

    def test_to_dict_keys(self):
        s = Student(student_id=1, student_code='ALU-2026-001',
                    first_name='Jane', last_name='Doe', email='jane@alu.edu')
        d = s.to_dict()
        for key in ['student_id', 'student_code', 'first_name', 'last_name', 'email', 'created_at']:
            self.assertIn(key, d)

    def test_str(self):
        s = Student(student_code='ALU-2026-001', first_name='Jane', last_name='Doe')
        self.assertEqual(str(s), 'ALU-2026-001 - Jane Doe')


class TestSubject(unittest.TestCase):

    def test_str(self):
        sub = Subject(subject_name='Mathematics')
        self.assertEqual(str(sub), 'Mathematics')

    def test_to_dict_keys(self):
        sub = Subject(subject_id=1, subject_name='Physics')
        d   = sub.to_dict()
        self.assertIn('subject_id', d)
        self.assertIn('subject_name', d)


class TestAssessment(unittest.TestCase):

    def test_str(self):
        a = Assessment(assessment_name='Quiz 1', max_score=50)
        self.assertEqual(str(a), 'Quiz 1 (max: 50)')

    def test_to_dict_keys(self):
        a = Assessment(assessment_id=1, subject_id=2,
                       assessment_name='Midterm', max_score=100, date_given='2026-03-01')
        d = a.to_dict()
        for key in ['assessment_id', 'subject_id', 'assessment_name', 'max_score', 'date_given']:
            self.assertIn(key, d)


if __name__ == '__main__':
    unittest.main()
