from model import Transaction
transactions = []

# Add transaction 
def addTransac(date, amount, type, category, note):
    transac = Transaction(date, amount, type, category, note)
    transactions.append(transac)

