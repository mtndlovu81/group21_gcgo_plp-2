# config/settings.py — Application configuration and constants

class Settings:
    # Database credentials
    DB_HOST = 'localhost'
    DB_USER = 'admin'
    DB_PASSWORD = 'admin123'
    DB_NAME = 'student_performance_db'

    # Teacher login passphrase
    TEACHER_PASSPHRASE = 'admin123'

    # Performance thresholds (percentage ranges)
    PERFORMANCE_THRESHOLDS = {
        'Excellent':         (80, 100),
        'Good':              (60, 79),
        'Average':           (40, 59),
        'Needs Improvement': (0,  39),
    }

    # Students below this % are flagged for intervention
    PASS_THRESHOLD = 40
