from views.menu_manager import MenuManager

class MockDB:
    pass

def main():
    db = MockDB()
    app = MenuManager(db)
    app.run()

if __name__ == "__main__":
    main()
