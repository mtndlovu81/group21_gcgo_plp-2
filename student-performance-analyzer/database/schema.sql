-- database/schema.sql — CREATE TABLE statements for student_performance_db

CREATE TABLE IF NOT EXISTS students (
    student_id   INT          PRIMARY KEY AUTO_INCREMENT,
    student_code VARCHAR(20)  UNIQUE NOT NULL,
    first_name   VARCHAR(50)  NOT NULL,
    last_name    VARCHAR(50)  NOT NULL,
    email        VARCHAR(100) UNIQUE,
    created_at   DATETIME     DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id   INT          PRIMARY KEY AUTO_INCREMENT,
    subject_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id   INT           PRIMARY KEY AUTO_INCREMENT,
    subject_id      INT           NOT NULL,
    assessment_name VARCHAR(100)  NOT NULL,
    max_score       DECIMAL(5,2)  NOT NULL DEFAULT 100,
    date_given      DATE          NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS topics (
    topic_id   INT          PRIMARY KEY AUTO_INCREMENT,
    subject_id INT          NOT NULL,
    topic_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

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
);
