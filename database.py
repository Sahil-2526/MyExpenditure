import sqlite3
import uuid
import streamlit as st

class Database:
    def __init__(self, db_name="myexpenditure.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER NOT NULL,
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
                uid INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                transaction_type TEXT NOT NULL,
                is_default INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                limit_amount REAL NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                FOREIGN KEY(category_id) REFERENCES categories(id),
                UNIQUE(category_id, month, year)
            )
        """)
    
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid INTEGER NOT NULL,
                name TEXT NOT NULL UNIQUE,
                target_amount REAL NOT NULL,
                deadline TEXT
            )
        """)
                
        self.connection.commit()

    def register(self, username, email, password):
        self.cursor.execute("""
            INSERT INTO users(username, email, password)
                VALUES (?, ?, ?)
                """,(username, email, password))
        self.connection.commit()

    def login(self, email, password):
        self.cursor.execute("""
            SELECT uid 
            FROM users 
            WHERE email = ? AND
            password = ?
                """,( email, password))
        user = self.cursor.fetchone()
        return user
    
#----------------- Category function ---------------
    def add_category(self, name, transaction_type, is_default):
        uid = st.session_state.uid
        self.cursor.execute("""
            INSERT INTO categories
            (uid, name, transaction_type, is_default)
            VALUES (?, ?, ?, ?)
        """, (uid, name, transaction_type, int(is_default)))

        self.connection.commit()

    def get_categories(self):
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM categories
            WHERE uid = ?
        """, (uid,))

        return self.cursor.fetchall()

    def find_category(self, name):
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM categories
            WHERE LOWER(name)=LOWER(?) AND
            uid = ?
        """, (name,uid))

        return self.cursor.fetchone()

    def remove_category(self, name):
        uid = st.session_state.uid
        self.cursor.execute("""
            DELETE
            FROM categories
            WHERE LOWER(name)=LOWER(?) AND
            uid = ?
        """, (name,uid))

        self.connection.commit()

# --------------------- Transaction function 

    def add_transaction(self, amount, date, transaction_type, category_id, note):
        uid = st.session_state.uid
        self.cursor.execute("""
            INSERT INTO transactions
            (uid, amount, date, transaction_type, category_id, note)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (uid, amount, date, transaction_type, category_id, note))

        self.connection.commit()
        return self.cursor.lastrowid

    def get_transactions(self):
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE uid = ?
            ORDER BY date DESC 
        """,(uid,))

        return self.cursor.fetchall()

    def find_transaction(self, transaction_id):
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE id = ? AND
            uid = ?
        """, (transaction_id, uid))

        return self.cursor.fetchone()


    def update_transaction(
       self,
        transaction_id,
        amount=None,
        date=None,
        transaction_type=None,
        category_id=None,
        note=None
    ):
        transaction = self.find_transaction(transaction_id)

        if transaction is None:
            return

        amount = amount if amount is not None else transaction[1]
        date = date if date is not None else transaction[2]
        transaction_type = (
            transaction_type if transaction_type is not None else transaction[3]
        )
        category_id = category_id if category_id is not None else transaction[4]
        note = note if note is not None else transaction[5]

        uid = st.session_state.uid

        self.cursor.execute("""
            UPDATE transactions
            SET
                amount = ?,
                date = ?,
                transaction_type = ?,
                category_id = ?,
                note = ?
            WHERE id = ? AND
                uid = ?
        """, (
            uid,
            amount,
            date,
            transaction_type,
            category_id,
            note,
            transaction_id
        ))

        self.connection.commit()

    def remove_transaction(self, transaction_id):
        uid = st.session_state.uid
        self.cursor.execute("""
            DELETE
            FROM transactions
            WHERE id = ? AND
            uid = ?
        """, (transaction_id,uid))

        self.connection.commit()

    def get_transactions_by_month(self, month, year):
        month = f"{month:02d}"
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE strftime('%m', date) = ?
            AND strftime('%Y', date) = ?
            AND uid = ?
            ORDER BY date
        """, (month, str(year), uid))

        return self.cursor.fetchall()

    def get_transactions_by_date(self, day, month, year):
        date = f"{year:04d}-{month:02d}-{day:02d}"
        uid = st.session_state.uid

        self.cursor.execute("""
            SELECT *
            FROM transactions
            WHERE date = ? 
            AND uid = ?
        """, (date, uid))
    
        return self.cursor.fetchall()

#------------------------ Budget funcitons ----------

    def add_budget(self, category_id, limit_amount, month, year):
        uid = st.session_state.uid

        self.cursor.execute("""
            INSERT INTO budgets
            (uid, category_id, limit_amount, month, year)
            VALUES (?, ?, ?, ?, ?)
        """, (uid, category_id, limit_amount, month, year))

        self.connection.commit()

    def get_budgets(self):
        uid = st.session_state.uid

        self.cursor.execute("""
            SELECT *
            FROM budgets
            WHERE uid = ?
            ORDER BY year DESC, month DESC
        """,(uid,))

        return self.cursor.fetchall()


    def find_budget(self, category_id, month, year):
        uid = st.session_state.uid

        self.cursor.execute("""
            SELECT *
            FROM budgets
            WHERE category_id = ?
            AND month = ?
            AND year = ?
            AND uid = ?
        """, (category_id, month, year, uid))

        return self.cursor.fetchone()

    def update_budget(self, category_id, limit_amount, month, year):
        uid = st.session_state.uid

        self.cursor.execute("""
            UPDATE budgets
            SET limit_amount = ?
            WHERE category_id = ?
            AND month = ?
            AND year = ?
            AND uid = ?
        """, (
            limit_amount,
            category_id,
            month,
            year,
            uid
        ))

        self.connection.commit()


    def remove_budget(self, category_id, month, year):
        uid = st.session_state.uid

        self.cursor.execute("""
            DELETE
            FROM budgets
            WHERE category_id = ?
            AND month = ?
            AND year = ?
            AND uid = ?
        """, (
            category_id,
            month,
            year,
            uid
        ))

        self.connection.commit()

# ------------------------- Goal functions --------

    def add_goal(self, name, target_amount, deadline):
        uid = st.session_state.uid

        self.cursor.execute("""
            INSERT INTO goals
            (uid, name, target_amount, deadline)
            VALUES (?, ?, ?, ?)
        """, (uid, name, target_amount, deadline))

        self.connection.commit()

    def get_goals(self):
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM goals
            WHERE uid = ?
            ORDER BY deadline
        """,(uid,))
    
        return self.cursor.fetchall()


    def find_goal(self, name):
        uid = st.session_state.uid
        self.cursor.execute("""
            SELECT *
            FROM goals
            WHERE LOWER(name) = LOWER(?)
            AND uid = ?
        """, (name,uid))

        return self.cursor.fetchone()

    def update_goal(self, name, target_amount, deadline):
        uid = st.session_state.uid
        self.cursor.execute("""
            UPDATE goals
            SET
                target_amount = ?,
                deadline = ?
            WHERE LOWER(name) = LOWER(?)
            AND uid = ?
        """, (
            target_amount,
            deadline,
            name,
            uid
        ))

        self.connection.commit()


    def remove_goal(self, name):
        uid = st.session_state.uid
        self.cursor.execute("""
            DELETE
            FROM goals
            WHERE LOWER(name) = LOWER(?)
            AND uid = ?
        """, (name,uid))

        self.connection.commit()