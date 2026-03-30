# services/data_importer.py — Bulk xlsx import
# Full implementation in Phase 7 (requires Subject/Assessment models from Phase 3
# and DatabaseManager from Phase 2)

class DataImporter:
    """Parses .xlsx files and batch-inserts student/score data into the database.

    Depends on DatabaseManager. Full implementation in Phase 7.
    """

    def __init__(self, db_manager):
        self.db = db_manager
        self.imported = 0
        self.errors = 0
        self.skipped = 0
