import openpyxl
from utils.validators import validate_email, validate_student_code, validate_score, validate_non_empty
from models.student import Student
from models.subject import Subject
from models.assessment import Assessment
from models.score import Score
from utils.display_helpers import progress_bar, print_error, print_success

class DataImporter:
    def __init__(self, students_list, subjects_list, assessments_list, scores_list):
        self.students = students_list
        self.subjects = subjects_list
        self.assessments = assessments_list
        self.scores = scores_list
        self.imported = 0
        self.errors = 0
        self.skipped = 0

    def import_xlsx(self, filepath):
        wb = openpyxl.load_workbook(filepath)
        sheet = wb.active
        headers = [cell.value for cell in sheet[1]]
        total_rows = sheet.max_row - 1

        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=1):
            row_data = dict(zip(headers, row))

            # --- Validate student info ---
            if not validate_student_code(row_data.get("student_code", "")) or \
               not validate_email(row_data.get("email", "")) or \
               not validate_non_empty(row_data.get("name", "")):
                print_error(f"Row {idx}: Invalid student data")
                self.errors += 1
                continue

            # --- Subject ---
            subject_name = row_data.get("subject")
            subject = next((s for s in self.subjects if s.name == subject_name), None)
            if not subject:
                subject = Subject(subject_name, subject_name)
                self.subjects.append(subject)

            # --- Assessment ---
            assessment_name = row_data.get("assessment")
            assessment = next((a for a in self.assessments if a.title == assessment_name), None)
            if not assessment:
                assessment = Assessment(assessment_name, subject_name, assessment_name, 100)
                self.assessments.append(assessment)

            # --- Student ---
            student_code = row_data.get("student_code")
            student = next((s for s in self.students if s.student_id == student_code), None)
            if not student:
                student = Student(student_code, row_data.get("name"))
                self.students.append(student)

            # --- Score ---
            score_value = row_data.get("score", 0)
            if not validate_score(score_value):
                print_error(f"Row {idx}: Invalid score {score_value}")
                self.errors += 1
                continue

            score = Score(student_code, assessment_name, score_value)
            self.scores.append(score)
            self.imported += 1

            # Show progress
            progress_bar(idx, total_rows)

        print("\nSummary:")
        print_success(f"Imported: {self.imported}")
        print(f"Skipped: {self.skipped}")
        print_error(f"Errors: {self.errors}")
