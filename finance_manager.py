from transaction import Transaction
from category import Category
from budget import Budget
from goal import Goal
from enums import CategoryType


class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.categories = []
        self.budgets = []
        self.goals = []
    
    # ----------------------- Transaction Functions -------------------------------------------------------
    # Add transaction 
    def add_transaction(self,transaction):
        transac = Transaction(transaction)
        self.transactions.append(transac)

    # View all transaction
    def view_transactions(self):
        return self.transactions
    
    # Calculate total_credit
    def total_credit(self):
        return sum(t.amount for t in self.transactions if t.category_type == CategoryType.CREDIT)

    # Calculate total_debit
    def total_debit(self):
        return sum(t.amount for t in self.transactions if t.category_type == CategoryType.DEBIT)
    
    # calculate balance
    def balance(self):
        return self.total_credit() - self.total_debit()
    
    # category wise spending
    def category_wise_spending(self):
        summary = {}
        for t in self.transactions:
            if t.category_type == CategoryType.DEBIT:
                summary[t.category] = summary.get(t.category, 0) + t.amount
        return summary
    
    # Get transaction by date
    def transaction_by_month(self, day, month, year):
        summary = []
        for t in self.transactions:
            if t.date.day == day and t.date.month == month and t.date.year == year:
                summary.append(t)
        return summary

    # Get transaction by month
    def transaction_by_month(self, month, year):
        summary = []
        for t in self.transactions:
            if t.date.month == month and t.date.year == year:
                summary.append(t)
        return summary
    
    # ---------------------------Category Functions----------------------------------------------------------