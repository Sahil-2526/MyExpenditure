from model import Transaction
transactions = []

# Add transaction 
def add_transaction(date, amount, type, category, note):
    transac = Transaction(date, amount, type, category, note)
    transactions.append(transac)

# View all transaction
def view_transaction():
    return transactions

# Calculate total_credit
def total_credit():
    return sum(t.amount for t in transactions if t.type == "Credit")

# Calculate total_debit
def total_debit():
    return sum(t.amount for t in transactions if t.type == "Debit")

# calculate balance
def balance():
    return total_credit()-total_debit()

# category wise spending
def category_wise_spending():
    summary = {}
    for t in transactions:
        if t.type == "Debit":
            summary[t.category] = summary.get(t.category, 0) + t.amount
    return summary