import os
import sys

# Importing real modules from your teammates
try:
    from utils.display_helpers import DisplayHelper
    from utils.validators import validate_menu_choice, validate_student_code
    from services.performance_analyzer import PerformanceAnalyzer
    from services.data_importer import DataImporter
except ImportError:
    # Fallback class if teammates' files are not yet fully merged in your branch
    class DisplayHelper:
        def print_header(self, title): print(f"\n╔{'═'*(len(title)+2)}╗\n║ {title} ║\n╚{'═'*(len(title)+2)}╝")
        def print_menu(self, title, options):
            self.print_header(title)
            for i, opt in enumerate(options, 1): print(f" [{i}] {opt}")
        def print_error(self, msg): print(f"\033[91mERROR: {msg}\033[0m")
        def clear_screen(self): os.system('cls' if os.name == 'nt' else 'clear')

class MenuManager:
    def __init__(self, db_manager):
        self.db = db_manager
        self.display = DisplayHelper()
        # Initializing services for linked phases (Phase 7 & 8)
        self.analyzer = PerformanceAnalyzer(self.db)
        self.importer = DataImporter(self.db)

    def run(self):
 yannick-menu-system
        """Phase 5: Main application entry point loop"""
        while True:
            self.display.clear_screen()
            self.display.print_header("STUDENT PERFORMANCE ANALYZER")
            print("\n [1] Teacher Login\n [2] Student Login\n [3] Exit")

        """Main loop for login and routing"""
        while True:
            self.display.clear_screen()
            print("STUDENT PERFORMANCE ANALYZER")
            print("[1] Teacher Login\n[2] Student Login\n[3] Exit")
 main
            
            choice = input("\nSelect an option: ")
            if choice == '1':
                self.show_teacher_login()
            elif choice == '2':
                self.show_student_login()
            elif choice == '3':
                print("Exiting... Goodbye!")
                sys.exit()
            else:
                self.display.print_error("Invalid choice. Try again.")
                input("Press Enter...")

    def show_teacher_login(self):
        """Phase 5 Requirement: Teacher login via passphrase"""
        password = input("Enter Teacher Passphrase: ")
        # Using a default placeholder; ideally this comes from config/settings.py
        if password == "admin123": 
            self.teacher_menu()
        else:
            self.display.print_error("Access Denied: Incorrect Passphrase.")
            input("Press Enter to continue...")

    def show_student_login(self):
        """Phase 5 Requirement: Student login via student_code"""
        code = input("Enter Student Code (e.g., ALU-2026-001): ")
        # In a fully linked app, we verify the code exists in the database here
        self.student_menu(code)

    def teacher_menu(self):
 yannick-menu-system
        """Phase 5 Requirement: Teacher Menu with 9 options"""

        """Teacher Menu"""
 main
        while True:
            options = [
                "Add Student Record", 
                "Bulk Import from Spreadsheet", 
                "View All Students",
                "Performance Dashboard", 
                "View Students Needing Help", 
                "Update Student Record",
                "Delete Student Record", 
                "Generate Summary Report", 
                "Logout"
            ]
            self.display.clear_screen()
            self.display.print_menu("TEACHER MAIN MENU", options)
            choice = input("\nSelect action: ")
            
            if choice == '9': # Logout
                break
            
            # Integration logic for Phase 7 (Bulk Import)
            if choice == '2':
                path = input("Enter path to .xlsx file: ")
                self.importer.import_from_xlsx(path)
            
            # Integration logic for Phase 8 (Dashboard)
            elif choice == '4':
                from views.dashboard_view import DashboardView
                dash = DashboardView(self.analyzer, self.display)
                dash.show_dashboard()
            
            else:
                print(f"\nFeature {choice} is linked to other implementation phases.")
            
            input("\nPress Enter to return to menu...")

    def student_menu(self, student_code):
 yannick-menu-system
        """Phase 5 Requirement: Student Portal with 4 options"""

        """Student Portal"""
 main
        while True:
            options = [
                "View My Grades", 
                "View Feedback", 
                "Topic Breakdown", 
                "Logout"
            ]
            self.display.clear_screen()
            self.display.print_menu(f"STUDENT PORTAL: {student_code}", options)
            choice = input("\nSelect action: ")
            
            if choice == '4': # Logout
                break
            
            print(f"\nFeature {choice} is currently under development.")
            input("Press Enter to return...")
