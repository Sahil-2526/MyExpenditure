from model import Transaction
transactions = []

# Add transaction 
def addTransac(date, amount, type, category, note):
    transac = Transaction(date, amount, type, category, note)
    transactions.append(transac)

# View all transaction
def viewTransac():
    return transactions

# Calculate total_credit
def total_credit():
    return sum(t.amount for t in transactions if t.type == "Credit")

# Calculate total_debit
def total_debit():
    return sum(t.amount for t in transactions if t.type == "Debit")
