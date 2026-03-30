# services/performance_analyzer.py — Class and student performance analytics

class PerformanceAnalyzer:
    """Calculates class-wide and per-student performance statistics from the database."""

    def __init__(self, db_manager):
        self.db = db_manager

    # ------------------------------------------------------------------
    # Class-wide statistics
    # ------------------------------------------------------------------

    def get_class_stats(self):
        """Return overall class statistics.

        Returns dict with: total_students, total_scores, class_average, pass_rate.
        """
        total_students = self.db.execute_query(
            "SELECT COUNT(*) AS n FROM students", fetch='one'
        )['n']

        row = self.db.execute_query(
            """
            SELECT
                COUNT(sc.score_id) AS total_scores,
                AVG((sc.score_value / a.max_score) * 100) AS class_average,
                SUM(CASE WHEN (sc.score_value / a.max_score) * 100 >= 40 THEN 1 ELSE 0 END)
                    * 100.0 / COUNT(*) AS pass_rate
            FROM scores sc
            JOIN assessments a ON sc.assessment_id = a.assessment_id
            """,
            fetch='one'
        )

        return {
            'total_students': total_students,
            'total_scores':   int(row['total_scores'] or 0),
            'class_average':  round(float(row['class_average'] or 0), 1),
            'pass_rate':      round(float(row['pass_rate'] or 0), 1),
        }

    def get_subject_averages(self):
        """Return per-subject statistics ordered by average score descending.

        Each dict has: subject_name, avg_score, min_score, max_score, student_count.
        """
        return self.db.execute_query(
            """
            SELECT
                sub.subject_name,
                ROUND(AVG((sc.score_value / a.max_score) * 100), 1) AS avg_score,
                ROUND(MIN((sc.score_value / a.max_score) * 100), 1) AS min_score,
                ROUND(MAX((sc.score_value / a.max_score) * 100), 1) AS max_score,
                COUNT(DISTINCT sc.student_id) AS student_count
            FROM scores sc
            JOIN assessments a  ON sc.assessment_id = a.assessment_id
            JOIN subjects   sub ON a.subject_id      = sub.subject_id
            GROUP BY sub.subject_id, sub.subject_name
            ORDER BY avg_score DESC
            """,
            fetch='all'
        ) or []

    def get_score_distribution(self):
        """Return count of students in each performance level based on their overall average.

        Returns dict: {'Excellent': n, 'Good': n, 'Average': n, 'Needs Improvement': n}
        """
        rows = self.db.execute_query(
            """
            SELECT
                CASE
                    WHEN avg_pct >= 80 THEN 'Excellent'
                    WHEN avg_pct >= 60 THEN 'Good'
                    WHEN avg_pct >= 40 THEN 'Average'
                    ELSE 'Needs Improvement'
                END AS level,
                COUNT(*) AS count
            FROM (
                SELECT sc.student_id,
                       AVG((sc.score_value / a.max_score) * 100) AS avg_pct
                FROM scores sc
                JOIN assessments a ON sc.assessment_id = a.assessment_id
                GROUP BY sc.student_id
            ) AS student_avgs
            GROUP BY level
            """,
            fetch='all'
        ) or []

        distribution = {'Excellent': 0, 'Good': 0, 'Average': 0, 'Needs Improvement': 0}
        for row in rows:
            distribution[row['level']] = int(row['count'])
        return distribution

    # ------------------------------------------------------------------
    # Struggling students
    # ------------------------------------------------------------------

    def get_struggling_students(self, threshold=40):
        """Return students who are below threshold in ANY single subject.

        One row per student-subject pair that is below threshold, so a student
        struggling in two subjects appears twice.
        Each dict has: student_id, student_code, first_name, last_name, avg_pct,
                       weakest_subject, weakest_topic, trend.
        """
        rows = self.db.execute_query(
            """
            SELECT
                st.student_id,
                st.student_code,
                st.first_name,
                st.last_name,
                sub.subject_id,
                sub.subject_name,
                ROUND(AVG((sc.score_value / a.max_score) * 100), 1) AS avg_pct
            FROM students st
            JOIN scores sc      ON st.student_id    = sc.student_id
            JOIN assessments a  ON sc.assessment_id = a.assessment_id
            JOIN subjects   sub ON a.subject_id     = sub.subject_id
            GROUP BY st.student_id, sub.subject_id
            HAVING avg_pct < %s
            ORDER BY avg_pct ASC
            """,
            (threshold,), fetch='all'
        ) or []

        results = []
        for row in rows:
            sid = row['student_id']
            weakest_topic = self.get_weakest_topic(sid, row['subject_id'])
            trend         = self.get_student_trend(sid)

            results.append({
                **row,
                'weakest_subject': row['subject_name'],
                'weakest_topic':   weakest_topic or '—',
                'trend':           trend,
            })
        return results

    # ------------------------------------------------------------------
    # Per-student analytics
    # ------------------------------------------------------------------

    def get_student_trend(self, student_id):
        """Return 'Improving', 'Declining', or 'Stable' based on last 3 scores."""
        rows = self.db.execute_query(
            """
            SELECT (sc.score_value / a.max_score) * 100 AS pct
            FROM scores sc
            JOIN assessments a ON sc.assessment_id = a.assessment_id
            WHERE sc.student_id = %s
            ORDER BY sc.recorded_at DESC
            LIMIT 3
            """,
            (student_id,), fetch='all'
        )
        if not rows or len(rows) < 2:
            return 'Stable'

        scores = [float(r['pct']) for r in rows]
        # rows are newest-first; compare oldest to newest
        if scores[0] > scores[-1]:
            return 'Improving'
        if scores[0] < scores[-1]:
            return 'Declining'
        return 'Stable'

    def get_weakest_topic(self, student_id, subject_id):
        """Return the topic name where the student scored lowest, or None."""
        row = self.db.execute_query(
            """
            SELECT t.topic_name,
                   AVG((sc.score_value / a.max_score) * 100) AS avg_pct
            FROM scores sc
            JOIN assessments a ON sc.assessment_id = a.assessment_id
            JOIN topics t      ON sc.topic_id      = t.topic_id
            WHERE sc.student_id = %s AND a.subject_id = %s AND sc.topic_id IS NOT NULL
            GROUP BY t.topic_id
            ORDER BY avg_pct ASC
            LIMIT 1
            """,
            (student_id, subject_id), fetch='one'
        )
        return row['topic_name'] if row else None

    def get_student_grades(self, student_id):
        """Return all scores for a student grouped by subject.

        Returns list of dicts with: subject_name, assessment_name, score_value,
                                    max_score, percentage, level.
        """
        return self.db.execute_query(
            """
            SELECT
                sub.subject_name,
                a.assessment_name,
                sc.score_value,
                a.max_score,
                ROUND((sc.score_value / a.max_score) * 100, 1) AS percentage
            FROM scores sc
            JOIN assessments a  ON sc.assessment_id = a.assessment_id
            JOIN subjects   sub ON a.subject_id      = sub.subject_id
            WHERE sc.student_id = %s
            ORDER BY sub.subject_name, a.date_given
            """,
            (student_id,), fetch='all'
        ) or []

    def get_student_topic_breakdown(self, student_id):
        """Return per-topic averages for a student across all subjects."""
        return self.db.execute_query(
            """
            SELECT
                sub.subject_name,
                t.topic_name,
                ROUND(AVG((sc.score_value / a.max_score) * 100), 1) AS avg_pct
            FROM scores sc
            JOIN assessments a  ON sc.assessment_id = a.assessment_id
            JOIN subjects   sub ON a.subject_id      = sub.subject_id
            JOIN topics     t   ON sc.topic_id       = t.topic_id
            WHERE sc.student_id = %s AND sc.topic_id IS NOT NULL
            GROUP BY sub.subject_id, t.topic_id
            ORDER BY sub.subject_name, avg_pct ASC
            """,
            (student_id,), fetch='all'
        ) or []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_weakest_subject(self, student_id):
        """Return the subject dict where the student's average is lowest."""
        return self.db.execute_query(
            """
            SELECT sub.subject_id, sub.subject_name,
                   AVG((sc.score_value / a.max_score) * 100) AS avg_pct
            FROM scores sc
            JOIN assessments a  ON sc.assessment_id = a.assessment_id
            JOIN subjects   sub ON a.subject_id      = sub.subject_id
            WHERE sc.student_id = %s
            GROUP BY sub.subject_id
            ORDER BY avg_pct ASC
            LIMIT 1
            """,
            (student_id,), fetch='one'
        )
