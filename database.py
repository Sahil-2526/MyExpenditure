import sqlite3

class Database:
    def __init__(self, db_name="myexpenditure.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                date TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                category_id INTEGER NOT NULL,
                note TEXT,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)
                
        self.connection.commit()