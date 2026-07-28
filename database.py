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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                transaction_type TEXT NOT NULL,
                is_default INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                limit_amount REAL NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)
    
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                target_amount REAL NOT NULL,
                deadline TEXT
            )
        """)
                
        self.connection.commit()


#----------------- Category function
    def add_category(self, name, transaction_type, is_default):
        self.cursor.execute("""
            INSERT INTO categories
            (name, transaction_type, is_default)
            VALUES (?, ?, ?)
        """, (name, transaction_type, int(is_default)))

        self.connection.commit()

    def get_categories(self):
        self.cursor.execute("""
            SELECT *
            FROM categories
        """)

        return self.cursor.fetchall()

    def find_category(self, name):
        self.cursor.execute("""
            SELECT *
            FROM categories
            WHERE LOWER(name)=LOWER(?)
        """, (name,))

        return self.cursor.fetchone()

    def remove_category(self, name):
        self.cursor.execute("""
            DELETE
            FROM categories
            WHERE LOWER(name)=LOWER(?)
        """, (name,))

        self.connection.commit()

# --------------------- Transaction function 

    def add_transaction(self, amount, date, transaction_type, category_id, note):
        self.cursor.execute("""
            INSERT INTO transactions
            (amount, date, transaction_type, category_id, note)
            VALUES (?, ?, ?, ?, ?)
        """, (amount, date, transaction_type, category_id, note))

        self.connection.commit()

    def get_transactions(self):
        self.cursor.execute("""
            SELECT *
            FROM transactions
            ORDER BY date DESC
        """)

        return self.cursor.fetchall()

    def find_transaction(self, transaction_id):
        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        return self.cursor.fetchone()


    def update_transaction(self, transaction_id, amount, date, transaction_type, category_id, note ):
        self.cursor.execute("""
            UPDATE transactions
            SET
                amount = ?,
                date = ?,
                transaction_type = ?,
                category_id = ?,
                note = ?
            WHERE id = ?
        """, (
            amount,
            date,
            transaction_type,
            category_id,
            note,
            transaction_id
        ))

        self.connection.commit()

    def remove_transaction(self, transaction_id):
        self.cursor.execute("""
            DELETE
            FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        self.connection.commit()

    def get_transactions_by_month(self, month, year):
        month = f"{month:02d}"

        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE strftime('%m', date) = ?
            AND strftime('%Y', date) = ?
            ORDER BY date
        """, (month, str(year)))

        return self.cursor.fetchall()

    def get_transactions_by_date(self, day, month, year):
        date = f"{year:04d}-{month:02d}-{day:02d}"

        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE date = ?
        """, (date,))
    
        return self.cursor.fetchall()

#------------------------ Budget funcitons ----------

    def add_budget(self, category_id, limit_amount, month, year):
        self.cursor.execute("""
            INSERT INTO budgets
            (category_id, limit_amount, month, year)
            VALUES (?, ?, ?, ?)
        """, (category_id, limit_amount, month, year))

        self.connection.commit()

    def get_budgets(self):
        self.cursor.execute("""
            SELECT *
            FROM budgets
            ORDER BY year DESC, month DESC
        """)

        return self.cursor.fetchall()


    def find_budget(self, category_id, month, year):
        self.cursor.execute("""
            SELECT *
            FROM budgets
            WHERE category_id = ?
            AND month = ?
            AND year = ?
        """, (category_id, month, year))

        return self.cursor.fetchone()

    def update_budget(self, category_id, limit_amount, month, year):
        self.cursor.execute("""
            UPDATE budgets
            SET limit_amount = ?
            WHERE category_id = ?
            AND month = ?
            AND year = ?
        """, (
            limit_amount,
            category_id,
            month,
            year
        ))

        self.connection.commit()


    def remove_budget(self, category_id, month, year):
        self.cursor.execute("""
            DELETE
            FROM budgets
            WHERE category_id = ?
            AND month = ?
            AND year = ?
        """, (
            category_id,
            month,
            year
        ))

        self.connection.commit()

# ------------------------- Goal functions --------

    def add_goal(self, name, target_amount, deadline):
        self.cursor.execute("""
            INSERT INTO goals
            (name, target_amount, deadline)
            VALUES (?, ?, ?)
        """, (name, target_amount, deadline))

        self.connection.commit()

    def get_goals(self):
        self.cursor.execute("""
            SELECT *
            FROM goals
            ORDER BY deadline
        """)
    
        return self.cursor.fetchall()


    def find_goal(self, name):
        self.cursor.execute("""
            SELECT *
            FROM goals
            WHERE LOWER(name) = LOWER(?)
        """, (name,))

        return self.cursor.fetchone()

    def update_goal(self, name, target_amount, deadline):
        self.cursor.execute("""
            UPDATE goals
            SET
                target_amount = ?,
                deadline = ?
            WHERE LOWER(name) = LOWER(?)
        """, (
            target_amount,
            deadline,
            name
        ))

        self.connection.commit()


    def remove_goal(self, name):
        self.cursor.execute("""
            DELETE
            FROM goals
            WHERE LOWER(name) = LOWER(?)
        """, (name,))

        self.connection.commit()