# views/dashboard_view.py — Teacher performance dashboard

from tabulate import tabulate
from colorama import Fore, Style
from models.score import Score


class DashboardView:
    """Renders the teacher-facing performance dashboard in the terminal."""

    BAR_WIDTH = 30  # max width of ASCII bar chart bars

    def __init__(self, analyzer, display):
        self.analyzer = analyzer
        self.display = display

    # ------------------------------------------------------------------
    # Main dashboard
    # ------------------------------------------------------------------

    def show_dashboard(self):
        self.display.clear_screen()
        self.display.print_header("PERFORMANCE DASHBOARD")

        stats = self.analyzer.get_class_stats()

        if stats['total_scores'] == 0:
            self.display.print_warning("No scores recorded yet. Add students and scores first.")
            input("\nPress Enter to continue...")
            return

        self._print_class_overview(stats)
        self._print_student_matrix()
        self._print_score_distribution()
        self._print_struggling_alert()

        input("\nPress Enter to continue...")

    def show_struggling_students(self):
        self.display.clear_screen()
        self.display.print_header("STUDENTS NEEDING HELP")

        students = self.analyzer.get_struggling_students()

        if not students:
            self.display.print_success("No students below the intervention threshold (40%). Great work!")
            input("\nPress Enter to continue...")
            return

        trend_icons = {'Improving': '↑', 'Declining': '↓', 'Stable': '→'}

        rows = [
            [
                s['student_code'],
                f"{s['first_name']} {s['last_name']}",
                self.display.color_by_level(
                    f"{s['avg_pct']}%",
                    Score.get_performance_level(float(s['avg_pct']))
                ),
                trend_icons.get(s['trend'], '→') + ' ' + s['trend'],
                s['weakest_subject'],
                s['weakest_topic'],
            ]
            for s in students
        ]

        headers = ["Code", "Name", "Average", "Trend", "Weakest Subject", "Weakest Topic"]
        print(tabulate(rows, headers=headers, tablefmt='grid'))
        print(f"\n{Fore.RED}{len(students)} student(s) need intervention.{Style.RESET_ALL}")
        input("\nPress Enter to continue...")

    # ------------------------------------------------------------------
    # Dashboard sections
    # ------------------------------------------------------------------

    def _print_class_overview(self, stats):
        avg   = stats['class_average']
        level = Score.get_performance_level(avg)

        print(f"\n{'='*50}")
        print(f"  CLASS OVERVIEW")
        print(f"{'='*50}")
        print(f"  Total students : {stats['total_students']}")
        print(f"  Total scores   : {stats['total_scores']}")
        print(f"  Class average  : {self.display.color_by_level(f'{avg}%', level)}")
        print(f"  Pass rate      : {stats['pass_rate']}%")
        print(f"{'='*50}\n")

    def _print_student_matrix(self):
        """Print one student × topic table per subject."""
        matrix = self.analyzer.get_dashboard_matrix()
        if not matrix:
            return

        missing_cell  = f"{Style.DIM}--- (MISSING){Style.RESET_ALL}"
        level_colors  = {
            'Excellent':         Fore.GREEN,
            'Good':              Fore.CYAN,
            'Average':           Fore.YELLOW,
            'Needs Improvement': Fore.RED,
        }

        print("  STUDENT × TOPIC MATRIX\n")

        for subj in matrix:
            topics   = subj['topics']
            students = subj['students']
            scores   = subj['scores']    # {(student_id, topic_id): avg_pct}
            averages = subj['averages']  # {student_id: avg_pct}

            if not students:
                continue

            print(f"  {Fore.WHITE}{Style.BRIGHT}{subj['subject_name'].upper()}{Style.RESET_ALL}")

            # Build table header: Student | topic1 | topic2 | ... | Avg
            headers = ["Student"] + [t['topic_name'] for t in topics] + ["Avg"]

            rows = []
            for st in students:
                sid  = st['student_id']
                name = f"{st['student_code']}  {st['first_name']} {st['last_name']}"

                cells = []
                for t in topics:
                    tid = t['topic_id']
                    pct = scores.get((sid, tid))
                    if pct is None:
                        cells.append(missing_cell)
                    else:
                        level = Score.get_performance_level(pct)
                        color = level_colors.get(level, '')
                        lbl   = 'NEEDS HELP' if level == 'Needs Improvement' else level
                        cells.append(f"{color}{pct:>5.1f}%  [{lbl}]{Style.RESET_ALL}")

                avg = averages.get(sid)
                if avg is not None:
                    level    = Score.get_performance_level(avg)
                    color    = level_colors.get(level, '')
                    avg_cell = f"{color}{avg:>5.1f}%{Style.RESET_ALL}"
                else:
                    avg_cell = missing_cell

                rows.append([name] + cells + [avg_cell])

            print(tabulate(rows, headers=headers, tablefmt='grid'))
            print()

    def _print_score_distribution(self):
        dist = self.analyzer.get_score_distribution()
        total = sum(dist.values())
        if total == 0:
            return

        print("  SCORE DISTRIBUTION\n")

        level_colors = {
            'Excellent':         Fore.GREEN,
            'Good':              Fore.BLUE,
            'Average':           Fore.YELLOW,
            'Needs Improvement': Fore.RED,
        }

        for level in ['Excellent', 'Good', 'Average', 'Needs Improvement']:
            count      = dist[level]
            proportion = count / total if total else 0
            filled     = int(self.BAR_WIDTH * proportion)
            bar        = '█' * filled + '░' * (self.BAR_WIDTH - filled)
            color      = level_colors[level]
            label      = f"{level:<20}"
            print(f"  {color}{label}{Style.RESET_ALL} {color}{bar}{Style.RESET_ALL}  {count} student(s)")

        print()

    def _print_struggling_alert(self):
        struggling = self.analyzer.get_struggling_students()
        count = len(struggling)
        if count > 0:
            print(f"{Fore.RED}  ⚠  {count} student(s) are below the intervention threshold (40%).{Style.RESET_ALL}")
            print(f"{Fore.RED}     Use 'Students Needing Help' for details.{Style.RESET_ALL}\n")
