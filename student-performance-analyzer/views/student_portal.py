# views/student_portal.py — Student-facing portal: grades, feedback, topic breakdown

from tabulate import tabulate
from colorama import Fore, Style
from models.score import Score


class StudentPortal:
    """Renders grade views, personalised feedback, and topic breakdown for a student."""

    def __init__(self, analyzer, display):
        self.analyzer = analyzer
        self.display = display

    # ------------------------------------------------------------------
    # F9 — View my grades
    # ------------------------------------------------------------------

    def show_grades(self, student):
        self.display.clear_screen()
        self.display.print_header(f"MY GRADES — {student['first_name']} {student['last_name']}")

        grades = self.analyzer.get_student_grades(student['student_id'])

        if not grades:
            self.display.print_warning("No grades recorded yet.")
            input("\nPress Enter to continue...")
            return

        # Group by subject
        subjects = {}
        for g in grades:
            subjects.setdefault(g['subject_name'], []).append(g)

        overall_scores = []

        for subject_name, rows in subjects.items():
            print(f"\n  {Fore.CYAN}{Style.BRIGHT}{subject_name}{Style.RESET_ALL}")

            table_rows = []
            for r in rows:
                pct   = float(r['percentage'])
                level = Score.get_performance_level(pct)
                table_rows.append([
                    r['assessment_name'],
                    f"{r['score_value']}",
                    f"{r['max_score']}",
                    f"{pct}%",
                    self.display.color_by_level(level, level),
                ])
                overall_scores.append(pct)

            print(tabulate(
                table_rows,
                headers=["Assessment", "Score", "Max", "Percentage", "Level"],
                tablefmt='grid'
            ))

        if overall_scores:
            overall_avg = sum(overall_scores) / len(overall_scores)
            level       = Score.get_performance_level(overall_avg)
            print(f"\n  Overall average: {self.display.color_by_level(f'{overall_avg:.1f}%', level)}")

        input("\nPress Enter to continue...")

    # ------------------------------------------------------------------
    # F10 — View feedback
    # ------------------------------------------------------------------

    def show_feedback(self, student):
        self.display.clear_screen()
        self.display.print_header(f"MY FEEDBACK — {student['first_name']} {student['last_name']}")

        sid = student['student_id']

        # Per-subject averages for this student
        subject_avgs = self.analyzer.db.execute_query(
            """
            SELECT sub.subject_id, sub.subject_name,
                   ROUND(AVG((sc.score_value / a.max_score) * 100), 1) AS avg_pct
            FROM scores sc
            JOIN assessments a  ON sc.assessment_id = a.assessment_id
            JOIN subjects   sub ON a.subject_id      = sub.subject_id
            WHERE sc.student_id = %s
            GROUP BY sub.subject_id
            ORDER BY avg_pct DESC
            """,
            (sid,), fetch='all'
        ) or []

        if not subject_avgs:
            self.display.print_warning("No grades to generate feedback for yet.")
            input("\nPress Enter to continue...")
            return

        all_pcts = []
        for row in subject_avgs:
            pct          = float(row['avg_pct'])
            subject_name = row['subject_name']
            level        = Score.get_performance_level(pct)
            weakest      = self.analyzer.get_weakest_topic(sid, row['subject_id'])
            all_pcts.append(pct)

            print(f"\n  {Fore.CYAN}{Style.BRIGHT}{subject_name}{Style.RESET_ALL} — "
                  f"{self.display.color_by_level(f'{pct}%', level)}")
            print(f"  {self._feedback_message(subject_name, pct, level, weakest)}")

        # Overall summary
        overall = sum(all_pcts) / len(all_pcts)
        overall_level = Score.get_performance_level(overall)
        print(f"\n{'─'*52}")
        print(f"  Overall: {self.display.color_by_level(f'{overall:.1f}%', overall_level)}")
        print(f"  {self._overall_summary(overall_level, student['first_name'])}")

        input("\nPress Enter to continue...")

    # ------------------------------------------------------------------
    # F11 — Topic breakdown
    # ------------------------------------------------------------------

    def show_topic_breakdown(self, student):
        self.display.clear_screen()
        self.display.print_header(f"TOPIC BREAKDOWN — {student['first_name']} {student['last_name']}")

        rows = self.analyzer.get_student_topic_breakdown(student['student_id'])

        if not rows:
            self.display.print_warning("No topic data recorded yet.")
            input("\nPress Enter to continue...")
            return

        # Group by subject
        subjects = {}
        for r in rows:
            subjects.setdefault(r['subject_name'], []).append(r)

        for subject_name, topics in subjects.items():
            print(f"\n  {Fore.CYAN}{Style.BRIGHT}{subject_name}{Style.RESET_ALL}")

            # Topics are already ordered ASC by avg_pct — first is weakest
            weakest_topic = topics[0]['topic_name']

            table_rows = []
            for t in topics:
                pct   = float(t['avg_pct'])
                level = Score.get_performance_level(pct)
                name  = t['topic_name']

                if name == weakest_topic:
                    name_display = f"{Fore.RED}{name} ◀ focus here{Style.RESET_ALL}"
                else:
                    name_display = name

                table_rows.append([
                    name_display,
                    self.display.color_by_level(f"{pct}%", level),
                    self.display.color_by_level(level, level),
                ])

            print(tabulate(
                table_rows,
                headers=["Topic", "Average", "Level"],
                tablefmt='grid'
            ))

            self.display.print_info(f"  Focus area: {weakest_topic} in {subject_name}")

        input("\nPress Enter to continue...")

    # ------------------------------------------------------------------
    # Feedback message helpers
    # ------------------------------------------------------------------

    def _feedback_message(self, subject, pct, level, weakest_topic):
        if level == 'Excellent':
            return (f"{Fore.GREEN}Outstanding work in {subject}! "
                    f"You're in the top tier. Keep pushing!{Style.RESET_ALL}")
        elif level == 'Good':
            return (f"{Fore.BLUE}Solid performance in {subject}. "
                    f"A little more effort and you'll be excellent!{Style.RESET_ALL}")
        elif level == 'Average':
            topic_hint = f" Focus on {weakest_topic}." if weakest_topic else ""
            return (f"{Fore.YELLOW}You're on the edge in {subject}.{topic_hint} "
                    f"Consider seeking study group help.{Style.RESET_ALL}")
        else:
            topic_hint = f" Focus on {weakest_topic}." if weakest_topic else ""
            return (f"{Fore.RED}ALERT: Your {subject} score is below 40%.{topic_hint} "
                    f"Please book office hours with your teacher immediately.{Style.RESET_ALL}")

    def _overall_summary(self, level, first_name):
        if level == 'Excellent':
            return f"{Fore.GREEN}You're excelling overall, {first_name}. Keep it up!{Style.RESET_ALL}"
        elif level == 'Good':
            return f"{Fore.BLUE}Good overall, {first_name}. Push a bit harder to reach excellence!{Style.RESET_ALL}"
        elif level == 'Average':
            return f"{Fore.YELLOW}You're in the average range, {first_name}. Stay consistent and seek help where needed.{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}You need urgent support, {first_name}. Please speak to your teacher as soon as possible.{Style.RESET_ALL}"
