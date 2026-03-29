from colorama import Fore, Style, init

init(autoreset=True)

# Colored text
def print_success(message):
    print(Fore.GREEN + message)

def print_error(message):
    print(Fore.RED + message)

def print_info(message):
    print(Fore.CYAN + message)

# Box-drawing wrapper
def draw_box(text):
    width = len(text) + 4
    print("+" + "-" * (width - 2) + "+")
    print(f"|  {text}  |")
    print("+" + "-" * (width - 2) + "+")

# Simple table display
def print_table(rows):
    for row in rows:
        print(" | ".join(str(col) for col in row))

# Progress bar for bulk imports
def progress_bar(current, total, bar_length=20):
    filled = int(bar_length * current // total)
    bar = "█" * filled + "-" * (bar_length - filled)
    print(f"[{bar}] {current}/{total}", end="\r")
