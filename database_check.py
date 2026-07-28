from database import Database

db = Database()
db.create_tables()

db.add_transaction(
    250,
    "2026-07-28",
    "DEBIT",
    1,
    "Lunch"
)

print(db.get_transactions())

print(db.find_transaction(1))

db.update_transaction(
    1,
    300,
    "2026-07-28",
    "DEBIT",
    1,
    "Lunch with friends"
)

print(db.find_transaction(1))

db.remove_transaction(1)

print(db.get_transactions())