# main.py — Entry point: initialise DB connection and launch the menu

from database.db_manager import DatabaseManager
from views.menu_manager import MenuManager


def main():
    db = DatabaseManager()
    if not db.connect():
        print("Failed to connect to the database. Check your MySQL settings in config/settings.py.")
        return

    try:
        app = MenuManager(db)
        app.run()
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
