# services/report_generator.py — Summary report generation

import os
from datetime import datetime
from models.score import Score


class ReportGenerator:
    """Generates a text-based summary report from PerformanceAnalyzer data."""

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def generate(self, save_to_file=False):
        """Build and print the report. Optionally save to a .txt file.

        Returns the report as a string.
        """
        lines = self._build_report()
        report = '\n'.join(lines)

        print(report)

        if save_to_file:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            return filename

        return None

    # ------------------------------------------------------------------
    # Internal builders
    # ------------------------------------------------------------------

    def _build_report(self):
        now   = datetime.now().strftime('%Y-%m-%d %H:%M')
        lines = []

        lines += [
            '=' * 60,
            '  STUDENT PERFORMANCE ANALYZER — SUMMARY REPORT',
            f'  Generated: {now}',
            '=' * 60,
        ]

        # Class overview
        stats = self.analyzer.get_class_stats()
        lines += [
            '',
            'CLASS OVERVIEW',
            '-' * 40,
            f"  Total students : {stats['total_students']}",
            f"  Total scores   : {stats['total_scores']}",
            f"  Class average  : {stats['class_average']}%",
            f"  Pass rate      : {stats['pass_rate']}%",
        ]

        # Subject breakdown
        subjects = self.analyzer.get_subject_averages()
        if subjects:
            lines += ['', 'SUBJECT BREAKDOWN', '-' * 40]
            for s in subjects:
                level = Score.get_performance_level(float(s['avg_score']))
                lines.append(
                    f"  {s['subject_name']:<20} avg: {s['avg_score']}%  "
                    f"min: {s['min_score']}%  max: {s['max_score']}%  "
                    f"[{level}]"
                )

        # Score distribution
        dist = self.analyzer.get_score_distribution()
        lines += ['', 'SCORE DISTRIBUTION', '-' * 40]
        for level in ['Excellent', 'Good', 'Average', 'Needs Improvement']:
            lines.append(f"  {level:<22}: {dist[level]} student(s)")

        # Struggling students
        struggling = self.analyzer.get_struggling_students()
        lines += ['', 'STUDENTS NEEDING INTERVENTION', '-' * 40]
        if struggling:
            for s in struggling:
                lines.append(
                    f"  {s['student_code']}  {s['first_name']} {s['last_name']:<15}  "
                    f"{s['weakest_subject']}: {s['avg_pct']}%  "
                    f"Trend: {s['trend']}  Weakest topic: {s['weakest_topic']}"
                )
        else:
            lines.append('  No students below intervention threshold.')

        lines += ['', '=' * 60]
        return lines
