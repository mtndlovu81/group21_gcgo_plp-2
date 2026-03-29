import sys

class MenuManager:
    def __init__(self, db_manager):
        self.db = db_manager

    def run(self):
        """Main loop that shows login screen and routes to menus."""
        print("\n=== STUDENT PERFORMANCE ANALYZER ===")
        while True:
            choice = self.show_login()
            if choice == "1":
                self.handle_teacher_login()
            elif choice == "2":
                self.handle_student_login()
            elif choice == "3":
                print("Exiting...")
                sys.exit()

    def show_login(self):
        print("\n1. Teacher Login\n2. Student Login\n3. Exit")
        return input("Select option: ").strip()

    def handle_teacher_login(self):
        # Implementation for Phase 5 login
        print("\nTeacher Login Selected")
        # Logic for passphrase goes here in next steps

    def handle_student_login(self):
        # Implementation for Phase 5 student access
        print("\nStudent Login Selected")
