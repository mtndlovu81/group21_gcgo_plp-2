import os
from models.student import Student

FILE_NAME = "students.txt"

# Create file if it does not exist
if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()

def get_performance(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Needs Improvement"

def add_student():
    student_id = raw_input("Enter ID: ")
    name = raw_input("Enter Name: ")

    try:
        score = int(raw_input("Enter Score: "))
    except:
        print("Invalid score")
        return

    student = Student(student_id, name, score)

    with open(FILE_NAME, "a") as f:
        f.write("{},{},{},{}\n".format(student.student_id, student.name, student.score, student.get_performance()))

    print("Student added successfully")

def view_students():
    print("\n--- Student Records ---")
    with open(FILE_NAME, "r") as f:
        for line in f:
            print(line.strip())

def update_student():
    student_id = raw_input("Enter ID to update: ")
    lines = []
    found = False

    with open(FILE_NAME, "r") as f:
        for line in f:
            data = line.strip().split(",")
            if data[0] == student_id:
                found = True
                name = raw_input("New name: ")
                try:
                    score = int(raw_input("New score: "))
                except:
                    print("Invalid score")
                    return
                performance = get_performance(score)
                line = "{},{},{},{}\n".format(student_id, name, score, performance)
            lines.append(line)

    if not found:
        print("Student not found")
        return

    with open(FILE_NAME, "w") as f:
        f.writelines(lines)

    print("Updated successfully")

def delete_student():
    student_id = raw_input("Enter ID to delete: ")
    lines = []
    found = False

    with open(FILE_NAME, "r") as f:
        for line in f:
            if line.startswith(student_id):
                found = True
                continue
            lines.append(line)

    if not found:
        print("Student not found")
        return

    with open(FILE_NAME, "w") as f:
        f.writelines(lines)

    print("Deleted successfully")

def menu():
    while True:
        print("\n=== Student Performance Analyzer ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")

        choice = raw_input("Choose: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option")

menu()
