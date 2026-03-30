# tests/test_db_manager.py — Unit tests for DatabaseManager

import unittest
from database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager()
        self.connected = self.db.connect()

    def tearDown(self):
        if self.connected:
            self.db.execute_query("DELETE FROM students WHERE student_code LIKE 'TEST-%'")
            self.db.execute_query("DELETE FROM subjects WHERE subject_name LIKE 'TestSubj%'")
            self.db.disconnect()

    def test_connection(self):
        self.assertTrue(self.connected)

    def test_create_tables_is_idempotent(self):
        """Calling create_tables() again on existing tables should not raise."""
        self.db.create_tables()

    def test_insert_and_retrieve_student(self):
        self.db.execute_query(
            "INSERT INTO students (student_code, first_name, last_name, email) VALUES (%s,%s,%s,%s)",
            ('TEST-2026-001', 'Unit', 'Test', 'unit@test.com')
        )
        row = self.db.execute_query(
            "SELECT * FROM students WHERE student_code = %s",
            ('TEST-2026-001',), fetch='one'
        )
        self.assertIsNotNone(row)
        self.assertEqual(row['first_name'], 'Unit')

    def test_cascade_delete_removes_scores(self):
        """Deleting a student should cascade-delete their scores."""
        sid = self.db.execute_query(
            "INSERT INTO students (student_code, first_name, last_name, email) VALUES (%s,%s,%s,%s)",
            ('TEST-2026-002', 'Cascade', 'Test', 'cascade@test.com')
        )
        subj_id = self.db.execute_query(
            "INSERT INTO subjects (subject_name) VALUES (%s)", ('TestSubjCascade',)
        )
        assess_id = self.db.execute_query(
            "INSERT INTO assessments (subject_id, assessment_name, max_score, date_given) "
            "VALUES (%s,%s,%s,%s)",
            (subj_id, 'TestAssessment', 100, '2026-01-01')
        )
        self.db.execute_query(
            "INSERT INTO scores (student_id, assessment_id, score_value) VALUES (%s,%s,%s)",
            (sid, assess_id, 75)
        )

        scores_before = self.db.execute_query(
            "SELECT * FROM scores WHERE student_id = %s", (sid,), fetch='all'
        )
        self.assertEqual(len(scores_before), 1)

        self.db.execute_query("DELETE FROM students WHERE student_id = %s", (sid,))

        scores_after = self.db.execute_query(
            "SELECT * FROM scores WHERE student_id = %s", (sid,), fetch='all'
        )
        self.assertEqual(len(scores_after), 0)


if __name__ == '__main__':
    unittest.main()
