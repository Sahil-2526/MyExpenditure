from model import Transaction
from category_type import CategoryType
transactions = []

# Add transaction 
def add_transaction(date, amount, category_type: CategoryType, category, note):
    transac = Transaction(date, amount, category_type, category, note)
    transactions.append(transac)

# View all transaction
def view_transactions():
    return transactions

# Calculate total_credit
def total_credit():
    return sum(t.amount for t in transactions if t.category_type == CategoryType.CREDIT)

# Calculate total_debit
def total_debit():
    return sum(t.amount for t in transactions if t.category_type == CategoryType.DEBIT)

# calculate balance
def balance():
    return total_credit()-total_debit()

# category wise spending
def category_wise_spending():
    summary = {}
    for t in transactions:
        if t.category_type == CategoryType.DEBIT:
            summary[t.category] = summary.get(t.category, 0) + t.amount
    return summary

# Get transaction by date
def transaction_by_month(day, month, year):
    summary = []
    for t in transactions:
        if t.date.day == day and t.date.month == month and t.date.year == year:
            summary.append(t)
    return summary


# Get transaction by month
def transaction_by_month(month, year):
    summary = []
    for t in transactions:
        if t.date.month == month and t.date.year == year:
            summary.append(t)
    return summary