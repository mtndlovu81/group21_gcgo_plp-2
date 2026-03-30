# views/menu_manager.py — Main menu navigation, login, and CRUD handlers

import sys
from tabulate import tabulate
from config.settings import Settings
from utils.display_helpers import DisplayHelper
from utils.validators import (
    validate_menu_choice, validate_email,
    validate_student_code, validate_non_empty, validate_score,
)
from services.data_importer import DataImporter
from services.performance_analyzer import PerformanceAnalyzer
from views.dashboard_view import DashboardView


class MenuManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.display = DisplayHelper()

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def run(self):
        """Main loop: show login screen and route to the correct portal."""
        while True:
            self.display.clear_screen()
            self.display.print_banner()
            self.display.print_menu("MAIN MENU", ["Teacher Login", "Student Login", "Exit"])

            choice = input("\nSelect an option: ").strip()
            valid, msg = validate_menu_choice(choice, 3)

            if not valid:
                self.display.print_error(msg)
                input("Press Enter to continue...")
                continue

            if choice == '1':
                self._teacher_login()
            elif choice == '2':
                self._student_login()
            elif choice == '3':
                self.display.print_info("Goodbye!")
                sys.exit(0)

    # ------------------------------------------------------------------
    # Login screens
    # ------------------------------------------------------------------

    def _teacher_login(self):
        self.display.clear_screen()
        self.display.print_header("TEACHER LOGIN")
        passphrase = input("Enter passphrase: ").strip()

        if passphrase == Settings.TEACHER_PASSPHRASE:
            self.display.print_success("Access granted.")
            input("Press Enter to continue...")
            self.teacher_menu()
        else:
            self.display.print_error("Incorrect passphrase. Access denied.")
            input("Press Enter to continue...")

    def _student_login(self):
        self.display.clear_screen()
        self.display.print_header("STUDENT LOGIN")
        code = input("Enter your student code (e.g. ALU-2026-001): ").strip().upper()

        student = self.db.execute_query(
            "SELECT * FROM students WHERE student_code = %s",
            (code,),
            fetch='one'
        )

        if student:
            self.display.print_success(f"Welcome, {student['first_name']} {student['last_name']}!")
            input("Press Enter to continue...")
            self.student_menu(student)
        else:
            self.display.print_error("Student code not found. Please check and try again.")
            input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # Teacher menu
    # ------------------------------------------------------------------

    def teacher_menu(self):
        options = [
            "Add Student",
            "Bulk Import (.xlsx)",
            "View All Students",
            "Performance Dashboard",
            "Students Needing Help",
            "Update Student Record",
            "Delete Student Record",
            "Generate Report",
            "Logout",
        ]

        analyzer  = PerformanceAnalyzer(self.db)
        dashboard = DashboardView(analyzer, self.display)

        handlers = {
            '1': self._add_student,
            '2': self._bulk_import,
            '3': self._view_all_students,
            '4': dashboard.show_dashboard,
            '5': dashboard.show_struggling_students,
            '6': self._update_student,
            '7': self._delete_student,
        }
        pending = {'8'}

        while True:
            self.display.clear_screen()
            self.display.print_menu("TEACHER MENU", options)
            choice = input("\nSelect an option: ").strip()

            valid, msg = validate_menu_choice(choice, len(options))
            if not valid:
                self.display.print_error(msg)
                input("Press Enter to continue...")
                continue

            if choice == '9':
                break
            elif choice in pending:
                self.display.print_warning(f"Feature [{choice}] coming in the next phase.")
                input("Press Enter to continue...")
            elif choice in handlers:
                handlers[choice]()

    # ------------------------------------------------------------------
    # Student menu
    # ------------------------------------------------------------------

    def student_menu(self, student):
        options = ["View My Grades", "View Feedback", "Topic Breakdown", "Logout"]

        while True:
            self.display.clear_screen()
            self.display.print_menu(f"STUDENT PORTAL — {student['first_name']}", options)
            choice = input("\nSelect an option: ").strip()

            valid, msg = validate_menu_choice(choice, len(options))
            if not valid:
                self.display.print_error(msg)
                input("Press Enter to continue...")
                continue

            if choice == '4':
                break

            self.display.print_warning(f"Feature [{choice}] coming in the next phase.")
            input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # F2 — Bulk import
    # ------------------------------------------------------------------

    def _bulk_import(self):
        self.display.clear_screen()
        self.display.print_header("BULK IMPORT (.xlsx)")
        self.display.print_info("A sample template is at: templates/sample_import.xlsx\n")

        file_path = input("Enter path to .xlsx file: ").strip()
        importer = DataImporter(self.db)
        importer.import_from_xlsx(file_path)
        input("\nPress Enter to continue...")

    # ------------------------------------------------------------------
    # F1 — Add student
    # ------------------------------------------------------------------

    def _add_student(self):
        self.display.clear_screen()
        self.display.print_header("ADD STUDENT")

        # Student code
        while True:
            code = input("Student code (e.g. ALU-2026-001): ").strip().upper()
            valid, msg = validate_student_code(code)
            if not valid:
                self.display.print_error(msg)
                continue
            if self.db.execute_query(
                "SELECT student_id FROM students WHERE student_code = %s", (code,), fetch='one'
            ):
                self.display.print_error(f"{code} already exists.")
                input("Press Enter to continue...")
                return
            break

        # First name
        while True:
            first_name = input("First name: ").strip()
            valid, msg = validate_non_empty(first_name, "First name")
            if valid:
                break
            self.display.print_error(msg)

        # Last name
        while True:
            last_name = input("Last name: ").strip()
            valid, msg = validate_non_empty(last_name, "Last name")
            if valid:
                break
            self.display.print_error(msg)

        # Email
        while True:
            email = input("Email: ").strip()
            valid, msg = validate_email(email)
            if valid:
                break
            self.display.print_error(msg)

        row_id = self.db.execute_query(
            "INSERT INTO students (student_code, first_name, last_name, email) VALUES (%s, %s, %s, %s)",
            (code, first_name, last_name, email)
        )
        if row_id:
            self.display.print_success(f"Student {code} added successfully (ID: {row_id}).")
        else:
            self.display.print_error("Failed to add student.")
        input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # F3 — View all students
    # ------------------------------------------------------------------

    def _view_all_students(self):
        self.display.clear_screen()
        self.display.print_header("ALL STUDENTS")

        students = self.db.execute_query(
            """
            SELECT s.student_code, s.first_name, s.last_name, s.email,
                   COUNT(sc.score_id) AS scores
            FROM students s
            LEFT JOIN scores sc ON s.student_id = sc.student_id
            GROUP BY s.student_id
            ORDER BY s.student_code
            """,
            fetch='all'
        )

        if not students:
            self.display.print_warning("No students found.")
            input("Press Enter to continue...")
            return

        headers = ["Code", "First Name", "Last Name", "Email", "Scores"]
        rows = [
            [s['student_code'], s['first_name'], s['last_name'], s['email'], s['scores']]
            for s in students
        ]

        page_size = 20
        for i in range(0, len(rows), page_size):
            print(tabulate(rows[i:i + page_size], headers=headers, tablefmt='grid'))
            if i + page_size < len(rows):
                input(f"Showing {i + page_size}/{len(rows)} — Press Enter for next page...")

        print(f"\nTotal: {len(rows)} student(s)")
        input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # F6 — Update student record
    # ------------------------------------------------------------------

    def _update_student(self):
        self.display.clear_screen()
        self.display.print_header("UPDATE STUDENT")

        code = input("Enter student code: ").strip().upper()
        student = self.db.execute_query(
            "SELECT * FROM students WHERE student_code = %s", (code,), fetch='one'
        )
        if not student:
            self.display.print_error("Student not found.")
            input("Press Enter to continue...")
            return

        print(f"\n  Code  : {student['student_code']}")
        print(f"  Name  : {student['first_name']} {student['last_name']}")
        print(f"  Email : {student['email']}\n")

        self.display.print_menu("What would you like to update?", [
            "First name", "Last name", "Email", "Add a score", "Cancel"
        ])
        choice = input("Select: ").strip()

        if choice == '1':
            while True:
                value = input("New first name: ").strip()
                valid, msg = validate_non_empty(value, "First name")
                if valid:
                    break
                self.display.print_error(msg)
            if input(f"Save '{value}'? (y/n): ").strip().lower() == 'y':
                self.db.execute_query(
                    "UPDATE students SET first_name = %s WHERE student_code = %s", (value, code)
                )
                self.display.print_success("First name updated.")

        elif choice == '2':
            while True:
                value = input("New last name: ").strip()
                valid, msg = validate_non_empty(value, "Last name")
                if valid:
                    break
                self.display.print_error(msg)
            if input(f"Save '{value}'? (y/n): ").strip().lower() == 'y':
                self.db.execute_query(
                    "UPDATE students SET last_name = %s WHERE student_code = %s", (value, code)
                )
                self.display.print_success("Last name updated.")

        elif choice == '3':
            while True:
                value = input("New email: ").strip()
                valid, msg = validate_email(value)
                if valid:
                    break
                self.display.print_error(msg)
            if input(f"Save '{value}'? (y/n): ").strip().lower() == 'y':
                self.db.execute_query(
                    "UPDATE students SET email = %s WHERE student_code = %s", (value, code)
                )
                self.display.print_success("Email updated.")

        elif choice == '4':
            self._add_score(student)

        input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # F7 — Delete student record
    # ------------------------------------------------------------------

    def _delete_student(self):
        self.display.clear_screen()
        self.display.print_header("DELETE STUDENT")

        code = input("Enter student code: ").strip().upper()
        student = self.db.execute_query(
            "SELECT * FROM students WHERE student_code = %s", (code,), fetch='one'
        )
        if not student:
            self.display.print_error("Student not found.")
            input("Press Enter to continue...")
            return

        print(f"\n  {student['student_code']} — {student['first_name']} {student['last_name']} ({student['email']})")
        self.display.print_warning("This will permanently delete the student and ALL their scores.")
        confirm = input("Type DELETE to confirm: ").strip()

        if confirm == 'DELETE':
            self.db.execute_query(
                "DELETE FROM students WHERE student_code = %s", (code,)
            )
            self.display.print_success("Student deleted successfully.")
        else:
            self.display.print_info("Deletion cancelled.")

        input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # Score helpers (used by _update_student → Add a score)
    # ------------------------------------------------------------------

    def _add_score(self, student):
        """Add a score for a student: pick/create subject → assessment → enter value → optional topic."""
        print("\n--- ADD SCORE ---")

        # Subject
        subjects = self.db.execute_query(
            "SELECT * FROM subjects ORDER BY subject_name", fetch='all'
        )
        if subjects:
            options = [s['subject_name'] for s in subjects] + ["Create new subject"]
            self.display.print_menu("Select subject", options)
            choice = input("Select: ").strip()
            valid, msg = validate_menu_choice(choice, len(options))
            if not valid:
                self.display.print_error(msg)
                return
            if int(choice) == len(options):
                name = input("New subject name: ").strip()
                subject_id = self.db.execute_query(
                    "INSERT INTO subjects (subject_name) VALUES (%s)", (name,)
                )
            else:
                subject_id = subjects[int(choice) - 1]['subject_id']
        else:
            name = input("No subjects yet. Enter subject name: ").strip()
            subject_id = self.db.execute_query(
                "INSERT INTO subjects (subject_name) VALUES (%s)", (name,)
            )

        # Assessment
        assessments = self.db.execute_query(
            "SELECT * FROM assessments WHERE subject_id = %s ORDER BY assessment_name",
            (subject_id,), fetch='all'
        )
        if assessments:
            options = [
                f"{a['assessment_name']} (max: {a['max_score']})" for a in assessments
            ] + ["Create new assessment"]
            self.display.print_menu("Select assessment", options)
            choice = input("Select: ").strip()
            valid, msg = validate_menu_choice(choice, len(options))
            if not valid:
                self.display.print_error(msg)
                return
            if int(choice) == len(options):
                assessment_id, max_score = self._create_assessment(subject_id)
            else:
                assessment_id = assessments[int(choice) - 1]['assessment_id']
                max_score = float(assessments[int(choice) - 1]['max_score'])
        else:
            print("No assessments yet for this subject.")
            assessment_id, max_score = self._create_assessment(subject_id)

        if not assessment_id:
            return

        # Score value
        while True:
            raw = input(f"Score (0 – {max_score}): ").strip()
            valid, msg = validate_score(raw, max_score)
            if valid:
                score_value = float(raw)
                break
            self.display.print_error(msg)

        # Optional topic
        topic_id = self._select_optional_topic(subject_id)

        row_id = self.db.execute_query(
            "INSERT INTO scores (student_id, assessment_id, score_value, topic_id) VALUES (%s, %s, %s, %s)",
            (student['student_id'], assessment_id, score_value, topic_id)
        )
        if row_id:
            self.display.print_success(f"Score {score_value}/{max_score} recorded.")
        else:
            self.display.print_error("Failed to record score.")

    def _create_assessment(self, subject_id):
        """Prompt for a new assessment. Returns (assessment_id, max_score) or (None, None)."""
        name = input("Assessment name (e.g. Quiz 1): ").strip()
        while True:
            raw = input("Max score (default 100): ").strip() or "100"
            try:
                max_score = float(raw)
                if max_score > 0:
                    break
                self.display.print_error("Max score must be greater than 0.")
            except ValueError:
                self.display.print_error("Enter a valid number.")
        date = input("Date (YYYY-MM-DD): ").strip()

        assessment_id = self.db.execute_query(
            "INSERT INTO assessments (subject_id, assessment_name, max_score, date_given) VALUES (%s, %s, %s, %s)",
            (subject_id, name, max_score, date)
        )
        return (assessment_id, max_score) if assessment_id else (None, None)

    def _select_optional_topic(self, subject_id):
        """Let the teacher link a score to a topic. Returns topic_id or None."""
        topics = self.db.execute_query(
            "SELECT * FROM topics WHERE subject_id = %s ORDER BY topic_name",
            (subject_id,), fetch='all'
        )
        options = ([t['topic_name'] for t in topics] if topics else []) + [
            "Create new topic", "Skip (no topic)"
        ]
        self.display.print_menu("Link to a topic? (optional)", options)
        choice = input("Select: ").strip()
        valid, _ = validate_menu_choice(choice, len(options))
        if not valid:
            return None

        idx = int(choice)
        skip_idx = len(options)       # last option = skip
        new_idx = len(options) - 1    # second-to-last = create new

        if idx == skip_idx:
            return None
        if idx == new_idx:
            name = input("New topic name: ").strip()
            return self.db.execute_query(
                "INSERT INTO topics (subject_id, topic_name) VALUES (%s, %s)",
                (subject_id, name)
            )
        return topics[idx - 1]['topic_id']
