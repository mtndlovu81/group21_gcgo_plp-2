# views/menu_manager.py — Main menu navigation and login

import sys
from config.settings import Settings
from utils.display_helpers import DisplayHelper
from utils.validators import validate_menu_choice


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

            # Handlers wired up in Phase 6 onwards
            self.display.print_warning(f"Feature [{choice}] coming in the next phase.")
            input("Press Enter to continue...")

    # ------------------------------------------------------------------
    # Student menu
    # ------------------------------------------------------------------

    def student_menu(self, student):
        options = [
            "View My Grades",
            "View Feedback",
            "Topic Breakdown",
            "Logout",
        ]

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

            # Handlers wired up in Phase 9
            self.display.print_warning(f"Feature [{choice}] coming in the next phase.")
            input("Press Enter to continue...")
