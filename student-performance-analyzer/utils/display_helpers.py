# utils/display_helpers.py — Terminal display utilities

import os
from colorama import Fore, Style, init

init(autoreset=True)


# --- Module-level helper functions (used by services) ---

def print_success(message):
    print(Fore.GREEN + message + Style.RESET_ALL)

def print_error(message):
    print(Fore.RED + message + Style.RESET_ALL)

def print_warning(message):
    print(Fore.YELLOW + message + Style.RESET_ALL)

def print_info(message):
    print(Fore.CYAN + message + Style.RESET_ALL)

def progress_bar(current, total, bar_length=20):
    """Print an in-place progress bar."""
    if total == 0:
        return
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"[{bar}] {current}/{total}", end="\r")


# --- DisplayHelper class (used by views) ---

class DisplayHelper:

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        """Display the app welcome banner."""
        print(Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════════════╗
║      STUDENT PERFORMANCE ANALYZER            ║
║      Group 21 — ALU Education Project        ║
╚══════════════════════════════════════════════╝
""" + Style.RESET_ALL)

    def print_header(self, title):
        """Draw a prominent section header."""
        width = len(title) + 4
        print(Fore.CYAN + "╔" + "═" * width + "╗")
        print(Fore.CYAN + "║  " + Style.BRIGHT + title + Style.RESET_ALL + Fore.CYAN + "  ║")
        print(Fore.CYAN + "╚" + "═" * width + "╝" + Style.RESET_ALL)

    def print_menu(self, title, options):
        """Draw a numbered options menu inside a box."""
        width = max(len(title), max(len(o) for o in options)) + 8
        border = "+" + "-" * width + "+"
        print(f"\n{border}")
        label = f"|  {Fore.CYAN}{Style.BRIGHT}{title}{Style.RESET_ALL}"
        print(label.ljust(width + len(border) - 1) + "|")
        print(border)
        for i, option in enumerate(options, 1):
            line = f"|  [{i}] {option}"
            print(line.ljust(width + 1) + "|")
        print(border)

    def print_success(self, message):
        print(Fore.GREEN + message + Style.RESET_ALL)

    def print_error(self, message):
        print(Fore.RED + message + Style.RESET_ALL)

    def print_warning(self, message):
        print(Fore.YELLOW + message + Style.RESET_ALL)

    def print_info(self, message):
        print(Fore.CYAN + message + Style.RESET_ALL)

    def color_by_level(self, text, level):
        """Return text wrapped in the color for a performance level."""
        colors = {
            "Excellent": Fore.GREEN,
            "Good": Fore.BLUE,
            "Average": Fore.YELLOW,
            "Needs Improvement": Fore.RED,
        }
        color = colors.get(level, "")
        return f"{color}{text}{Style.RESET_ALL}"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
