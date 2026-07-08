import sqlite3

class Database:
    def __init__(self, db_name="myexpenditure.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

