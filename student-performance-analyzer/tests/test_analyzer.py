# tests/test_analyzer.py — Unit tests for PerformanceAnalyzer

import unittest
from database.db_manager import DatabaseManager
from services.performance_analyzer import PerformanceAnalyzer


class TestPerformanceAnalyzer(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager()
        self.db.connect()
        self.analyzer = PerformanceAnalyzer(self.db)
        self._insert_test_data()

    def tearDown(self):
        self.db.execute_query("DELETE FROM students WHERE student_code LIKE 'TEST-%'")
        self.db.execute_query("DELETE FROM subjects WHERE subject_name LIKE 'TestSubj%'")
        self.db.disconnect()

    def _insert_test_data(self):
        self.s1_id = self.db.execute_query(
            "INSERT INTO students (student_code, first_name, last_name, email) VALUES (%s,%s,%s,%s)",
            ('TEST-2026-A01', 'Alice', 'Analyzer', 'alice@test.com')
        )
        self.s2_id = self.db.execute_query(
            "INSERT INTO students (student_code, first_name, last_name, email) VALUES (%s,%s,%s,%s)",
            ('TEST-2026-A02', 'Brian', 'Analyzer', 'brian@test.com')
        )
        subj_id = self.db.execute_query(
            "INSERT INTO subjects (subject_name) VALUES (%s)", ('TestSubjAnalyzer',)
        )
        self.assess_id = self.db.execute_query(
            "INSERT INTO assessments (subject_id, assessment_name, max_score, date_given) "
            "VALUES (%s,%s,%s,%s)",
            (subj_id, 'Test Quiz', 100, '2026-01-01')
        )
        # Alice = 90 (Excellent), Brian = 30 (Needs Improvement)
        self.db.execute_query(
            "INSERT INTO scores (student_id, assessment_id, score_value) VALUES (%s,%s,%s)",
            (self.s1_id, self.assess_id, 90)
        )
        self.db.execute_query(
            "INSERT INTO scores (student_id, assessment_id, score_value) VALUES (%s,%s,%s)",
            (self.s2_id, self.assess_id, 30)
        )

    def test_get_class_stats_returns_expected_keys(self):
        stats = self.analyzer.get_class_stats()
        for key in ['total_students', 'total_scores', 'class_average', 'pass_rate']:
            self.assertIn(key, stats)

    def test_get_class_stats_values(self):
        stats = self.analyzer.get_class_stats()
        self.assertGreaterEqual(stats['total_students'], 2)
        self.assertGreaterEqual(stats['total_scores'], 2)

    def test_get_struggling_students_flags_below_threshold(self):
        struggling = self.analyzer.get_struggling_students(threshold=40)
        codes = [s['student_code'] for s in struggling]
        self.assertIn('TEST-2026-A02', codes)
        self.assertNotIn('TEST-2026-A01', codes)

    def test_get_student_trend_returns_valid_value(self):
        trend = self.analyzer.get_student_trend(self.s1_id)
        self.assertIn(trend, ['Improving', 'Stable', 'Declining'])

    def test_get_student_trend_improving(self):
        """Add three improving scores and check trend."""
        for score in [40, 60, 80]:
            self.db.execute_query(
                "INSERT INTO scores (student_id, assessment_id, score_value) VALUES (%s,%s,%s)",
                (self.s1_id, self.assess_id, score)
            )
        trend = self.analyzer.get_student_trend(self.s1_id)
        self.assertEqual(trend, 'Improving')

    def test_get_student_trend_declining(self):
        """Add three declining scores and check trend."""
        for score in [80, 60, 40]:
            self.db.execute_query(
                "INSERT INTO scores (student_id, assessment_id, score_value) VALUES (%s,%s,%s)",
                (self.s2_id, self.assess_id, score)
            )
        trend = self.analyzer.get_student_trend(self.s2_id)
        self.assertEqual(trend, 'Declining')


if __name__ == '__main__':
    unittest.main()
