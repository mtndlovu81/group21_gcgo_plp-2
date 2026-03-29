import os
import sys

try:
    from utils.display_helpers import DisplayHelper
except ImportError:
    class DisplayHelper:
        def print_menu(self, title, options):
            print(f"\n=== {title} ===")
            for i, opt in enumerate(options, 1): print(f"[{i}] {opt}")
        def clear_screen(self): os.system('clear')

class MenuManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.display = DisplayHelper()

    def run(self):
        """Phase 5: Main loop for login and routing"""
        while True:
            self.display.clear_screen()
            print("🎓 STUDENT PERFORMANCE ANALYZER")
            print("[1] Teacher Login\n[2] Student Login\n[3] Exit")
            
            choice = input("\nSelect an option: ")
            if choice == '1':
                self.show_teacher_login()
            elif choice == '2':
                self.show_student_login()
            elif choice == '3':
                sys.exit()

    def show_teacher_login(self):
        # Teacher login requires a passphrase per Phase 5 specs
        password = input("Enter Teacher Passphrase: ")
        if password == "admin123": 
            self.teacher_menu()
        else:
            print("Access Denied.")
            input("Press Enter...")

    def show_student_login(self):
        # Student login requires student_code per Phase 5 specs
        code = input("Enter Student Code (e.g., ALU-2026-001): ")
        self.student_menu(code)

    def teacher_menu(self):
        """Teacher Menu with all 9 required actions"""
        while True:
            options = [
                "Add Student", "Bulk Import", "View All Students",
                "Dashboard", "Students Needing Help", "Update Student",
                "Delete Student", "Generate Report", "Logout"
            ]
            self.display.print_menu("TEACHER MENU", options)
            choice = input("\nSelect: ")
            if choice == '9': break
            print(f"\nFeature {choice} is pending implementation.")
            input("Press Enter...")

    def student_menu(self, student_code):
        """Student Portal with 4 required actions"""
        while True:
            options = ["View My Grades", "View Feedback", "Topic Breakdown", "Logout"]
            self.display.print_menu(f"STUDENT PORTAL ({student_code})", options)
            choice = input("\nSelect: ")
            if choice == '4': break
            print(f"\nFeature {choice} is pending implementation.")
            input("Press Enter...")
