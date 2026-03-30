# database/db_manager.py — MySQL connection and CRUD operations

import mysql.connector
from mysql.connector import Error
from config.settings import Settings


class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Open the MySQL connection and create tables if they don't exist."""
        try:
            self.connection = mysql.connector.connect(
                host=Settings.DB_HOST,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD,
                database=Settings.DB_NAME,
            )
            self.cursor = self.connection.cursor(dictionary=True)
            self.create_tables()
            return True
        except Error as e:
            print(f"[DB] Connection failed: {e}")
            return False

    def disconnect(self):
        """Close cursor and connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
        except Error as e:
            print(f"[DB] Error closing connection: {e}")

    def create_tables(self):
        """Create all tables if they do not already exist."""
        statements = [
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id   INT          PRIMARY KEY AUTO_INCREMENT,
                student_code VARCHAR(20)  UNIQUE NOT NULL,
                first_name   VARCHAR(50)  NOT NULL,
                last_name    VARCHAR(50)  NOT NULL,
                email        VARCHAR(100) UNIQUE,
                created_at   DATETIME     DEFAULT NOW()
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id   INT          PRIMARY KEY AUTO_INCREMENT,
                subject_name VARCHAR(100) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id   INT          PRIMARY KEY AUTO_INCREMENT,
                subject_id      INT          NOT NULL,
                assessment_name VARCHAR(100) NOT NULL,
                max_score       DECIMAL(5,2) NOT NULL DEFAULT 100,
                date_given      DATE         NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS topics (
                topic_id   INT          PRIMARY KEY AUTO_INCREMENT,
                subject_id INT          NOT NULL,
                topic_name VARCHAR(100) NOT NULL,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS scores (
                score_id      INT          PRIMARY KEY AUTO_INCREMENT,
                student_id    INT          NOT NULL,
                assessment_id INT          NOT NULL,
                score_value   DECIMAL(5,2) NOT NULL,
                topic_id      INT,
                recorded_at   DATETIME     DEFAULT NOW(),
                FOREIGN KEY (student_id)    REFERENCES students(student_id)       ON DELETE CASCADE,
                FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE,
                FOREIGN KEY (topic_id)      REFERENCES topics(topic_id)           ON DELETE SET NULL
            )
            """,
        ]
        try:
            for statement in statements:
                self.cursor.execute(statement)
            self.connection.commit()
        except Error as e:
            print(f"[DB] Error creating tables: {e}")

    def execute_query(self, query, params=None, fetch=None):
        """Run a query and optionally return results.

        Args:
            query  (str):  SQL query string with %s placeholders.
            params (tuple): Values to bind to placeholders.
            fetch  (str):  'one', 'all', or None (for INSERT/UPDATE/DELETE).

        Returns:
            For SELECT: dict or list of dicts.
            For INSERT: lastrowid.
            For UPDATE/DELETE: rowcount.
            On error: None.
        """
        try:
            self.cursor.execute(query, params or ())
            if fetch == 'one':
                return self.cursor.fetchone()
            if fetch == 'all':
                return self.cursor.fetchall()
            self.connection.commit()
            return self.cursor.lastrowid if self.cursor.lastrowid else self.cursor.rowcount
        except Error as e:
            print(f"[DB] Query error: {e}")
            self.connection.rollback()
            return None
