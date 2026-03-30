# tests/test_importer.py — Unit tests for DataImporter

import os
import unittest
import openpyxl
from database.db_manager import DatabaseManager
from services.data_importer import DataImporter

VALID_FILE   = 'tests/test_valid_import.xlsx'
INVALID_FILE = 'tests/test_invalid_import.xlsx'


def _make_valid_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['student_code', 'first_name', 'last_name', 'email',
               'subject', 'assessment_name', 'max_score', 'score', 'topic', 'date'])
    ws.append(['TEST-2026-001', 'Import', 'Valid', 'valid@test.com',
               'TestImportSubj', 'Quiz 1', 100, 75, 'Topic A', '2026-01-01'])
    ws.append(['INVALID-CODE', '', '', 'bad-email',   # invalid row — should be skipped
               'TestImportSubj', 'Quiz 1', 100, 75, '', '2026-01-01'])
    wb.save(path)


def _make_missing_columns_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['student_code', 'first_name'])   # missing required columns
    ws.append(['TEST-2026-001', 'Test'])
    wb.save(path)


class TestDataImporter(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager()
        self.db.connect()
        _make_valid_xlsx(VALID_FILE)
        _make_missing_columns_xlsx(INVALID_FILE)

    def tearDown(self):
        self.db.execute_query("DELETE FROM students WHERE student_code LIKE 'TEST-%'")
        self.db.execute_query("DELETE FROM subjects WHERE subject_name = 'TestImportSubj'")
        for f in [VALID_FILE, INVALID_FILE]:
            if os.path.exists(f):
                os.remove(f)
        self.db.disconnect()

    def test_import_valid_file(self):
        importer = DataImporter(self.db)
        imported, skipped, errors = importer.import_from_xlsx(VALID_FILE)
        self.assertEqual(imported, 1)
        self.assertEqual(errors, 1)   # the invalid row

    def test_import_missing_columns_returns_error(self):
        importer = DataImporter(self.db)
        imported, skipped, errors = importer.import_from_xlsx(INVALID_FILE)
        self.assertEqual(imported, 0)
        self.assertEqual(errors, 1)

    def test_import_nonexistent_file(self):
        importer = DataImporter(self.db)
        imported, skipped, errors = importer.import_from_xlsx('does_not_exist.xlsx')
        self.assertEqual(imported, 0)
        self.assertEqual(errors, 1)

    def test_import_creates_student_in_db(self):
        DataImporter(self.db).import_from_xlsx(VALID_FILE)
        student = self.db.execute_query(
            "SELECT * FROM students WHERE student_code = %s",
            ('TEST-2026-001',), fetch='one'
        )
        self.assertIsNotNone(student)
        self.assertEqual(student['first_name'], 'Import')


if __name__ == '__main__':
    unittest.main()
