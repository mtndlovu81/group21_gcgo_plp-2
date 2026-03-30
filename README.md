# Student Performance Analyzer

A command-line application that helps teachers track student performance and identify struggling students early — ensuring no student is left behind, even in high student-to-teacher ratio classrooms common across African schools.

## Problem Statement

In many African countries, classrooms have student-to-teacher ratios as high as 60:1. Teachers simply cannot track every student's progress across multiple subjects, assessments, and topics manually. By the time a struggling student is noticed, it's often too late for meaningful intervention.

The Student Performance Analyzer solves this by automating performance tracking, surfacing data-driven insights through a terminal dashboard, and alerting teachers the moment a student falls behind — so they can intervene just in time.

## Features

### Teacher Portal

- Add student records one at a time or in bulk via spreadsheet (.xlsx) import
- View, update, and delete student records
- Terminal-based performance dashboard with color-coded analytics
- Early-warning system that automatically flags struggling students
- Subject and topic-level performance breakdowns
- Summary report generation

### Student Portal

- View personal grades organized by subject
- Receive personalized feedback based on performance level
- See topic-by-topic breakdown highlighting areas to focus on

### Performance Levels

- Excellent (80–100%) — Keep it up
- Good (60–79%) — Monitor progress
- Average (40–59%) — Consider additional support
- Needs Improvement (Below 40%) — Book office hours immediately

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.10+ |
| Database | MySQL 8.0 |
| Spreadsheet Parsing | openpyxl |
| Terminal UI | colorama, tabulate |
| Testing | unittest |
| Version Control | Git / GitHub |

## Installation

### Prerequisites

- Python 3.10 or higher installed on your machine
- MySQL 8.0 installed and running
- Git installed

### Step 1: Clone the repository
```bash
git clone https://github.com/your-username/student-performance-analyzer.git
cd student-performance-analyzer
```

### Step 2: Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set up the MySQL database

Log into MySQL and create the database:
```sql
CREATE DATABASE student_performance_db;
```

Then open `config/settings.py` and update the credentials to match your local MySQL setup:
```python
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'your_password_here'
DB_NAME = 'student_performance_db'
```

### Step 5: Run the application
```bash
python main.py
```

The application will automatically create all required tables on first run.

## Usage

When you launch the app, you will see a login screen:
```
+======================================+
|   Student Performance Analyzer       |
+======================================+
|   [1] Teacher Login                  |
|   [2] Student Login                  |
|   [3] Exit                           |
+======================================+
```

As a Teacher: Log in with the teacher passphrase to access the full menu — add students, import spreadsheets, view the dashboard, and identify students who need help.

As a Student: Log in with your student code (e.g. ALU-2026-001) to view your grades, read personalized feedback, and see which topics to focus on.

Bulk Import: Prepare a `.xlsx` file with these columns: `student_code | first_name | last_name | email | subject | assessment_name | max_score | score | topic | date`. A sample template is provided in `templates/sample_import.xlsx`.

## Project Structure
```
student-performance-analyzer/
├── main.py                    # Entry point — run this to start
├── requirements.txt           # Python dependencies
├── README.md
├── .gitignore
├── config/
│   └── settings.py            # DB credentials, thresholds
├── models/
│   ├── student.py             # Student class
│   ├── subject.py             # Subject class
│   ├── assessment.py          # Assessment class
│   └── score.py               # Score class
├── database/
│   ├── db_manager.py          # MySQL connection and CRUD
│   └── schema.sql             # Table definitions
├── services/
│   ├── performance_analyzer.py
│   ├── data_importer.py
│   └── report_generator.py
├── views/
│   ├── menu_manager.py        # Navigation and login
│   ├── dashboard_view.py      # Teacher dashboard
│   └── student_portal.py      # Student view
├── utils/
│   ├── validators.py          # Input validation
│   └── display_helpers.py     # Terminal formatting
├── templates/
│   └── sample_import.xlsx     # Import template
└── tests/
    ├── test_models.py
    ├── test_db_manager.py
    ├── test_analyzer.py
    └── test_importer.py
```

## Running Tests
```bash
# Run all tests
python -m unittest discover tests/

# Run a specific test file
python -m unittest tests.test_models

# Verbose output
python -m unittest discover tests/ -v
```

## Team — Group 21 (Education)

- Mthabisi Ndlovu
- Muuse Muuse
- Nathan Nduati
- Yannick Mutunzi

## Mission Alignment

This project supports ALU's Education mission and SDG 4 (Quality Education) by giving teachers in resource-constrained environments a practical, data-driven tool to ensure equitable academic support for every student.

## Credits

This project was built as part of the Peer Learning Project (PLP 2) at African Leadership University, BSE Year 1, Trimester 2.
