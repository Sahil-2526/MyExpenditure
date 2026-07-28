from enums import TransactionType

class FinanceManager:
    def __init__(self, db):
        self.db = db
    
    # ----------------------- Transaction Functions -------------------------------------------------------
    # Add transaction 
    def add_transaction(self,transaction):
        self.db.add_transaction(
            transaction.amount,
            transaction.date.isoformat(),
            transaction.transaction_type.value,
            transaction.category.id,
            transaction.note
        )

    # View all transaction
    def get_all_transactions(self):
        return self.db.get_transactions()
    
    # Get single transaction 
    def get_transaction(self, transaction_id):
        return self.db.find_transaction(transaction_id)
    
    # Calculate total_credit
    def total_credit(self):
        transactions = self.db.get_transactions()
        return sum(t.amount for t in transactions if t.transaction_type == TransactionType.CREDIT)

    # Calculate total_debit
    def total_debit(self):
        transactions = self.db.get_transactions()
        return sum(t.amount for t in transactions if t.transaction_type == TransactionType.DEBIT)
    
    # calculate balance
    def balance(self):
        return self.total_credit() - self.total_debit()
    
    # category wise spending
    def category_wise_spending(self):
        transactions = self.db.get_transactions()
        summary = {}
        for t in transactions:
            if t.transaction_type == TransactionType.DEBIT:
                summary[t.category.name] = summary.get(t.category.name, 0) + t.amount
        return summary
    
    # Get transaction by date
    def transaction_by_date(self, day, month, year):
        transactions = self.db.get_transactions()
        summary = []
        for t in transactions:
            if t.date.day == day and t.date.month == month and t.date.year == year:
                summary.append(t)
        return summary

    # Get transaction by month
    def transaction_by_month(self, month, year):
        transactions = self.db.get_transactions()
        summary = []
        for t in transactions:
            if t.date.month == month and t.date.year == year:
                summary.append(t)
        return summary
    
    # Edit transaction 
    def edit_transaction(self, transaction_id, amount = None, date = None, transaction_type = None, category_id = None, note = None ):
        self.db.update_transaction(
            transaction_id,
            amount,
            date.isoformat() if date else None,
            transaction_type.value if transaction_type else None,
            category_id,
            note
        )

    # ---------------------------Category Functions----------------------------------------------------------
    # Add category
    def add_category(self, category):
        self.db.add_category(
            category.name,
            category.transaction_type.value,
            category.is_default
        )

    # Remove category
    def remove_category(self, category_name):
       self.db.remove_category(category_name)
    
    # Get all categories
    def get_all_categories(self):
        return self.db.get_categories()
    
    # Get single transaction
    def find_category(self, category_name):
        return self.db.find_category(category_name)
    
    # ------------------------------Budget Functions--------------------------------------------------------------
    # Add budget
    def add_budget(self, budget):
        self.db.add_budget(
            budget.category.id,
            budget.limit_amount,
            budget.month,
            budget.year
        )
 
    # Remove Budget
    def remove_budget(self, category_id, month, year):
        self.db.remove_budget(
            category_id,
            month,
            year
        )

    # Get all budgets
    def get_all_budgets(self):
        return self.db.get_budgets()

    # Get budget by name and month of a year
    def get_budget(self, category_id, month, year):
       return self.db.find_budget(
            category_id,
            month,
            year
        )
    
    # Summarize a budget in detail 
    def check_budget(self, category_name, month, year):
        category = self.find_category(category_name)
        if category is None:
            print("Category not found.")
            return
        budget = self.get_budget(category.id, month, year)
        if budget is None:
            print("Budget not found.")
            return
        spent = 0
        transactions = self.db.get_transactions()
        for transaction in transactions:
            if (
                transaction.category.name.lower() == category_name.lower()
                and transaction.date.month == month
                and transaction.date.year == year
                and transaction.transaction_type == TransactionType.DEBIT
            ):
                spent += transaction.amount

        remaining = budget.limit_amount - spent

        print(f"Category  : {category_name}")
        print(f"Budget    : ₹{budget.limit_amount}")
        print(f"Spent     : ₹{spent}")
        print(f"Remaining : ₹{remaining}")
        if remaining >= 0:
            print("Status    : Within Budget")
        else:
            print(f"Status    : Over Budget by ₹{-remaining}")

        return {
        "category": category_name,
        "budget": budget.limit_amount,
        "spent": spent,
        "remaining": remaining,
        "status": remaining >= 0
    }


    # -------------------------------------Goal functions--------------------------------------------------
    # Add goal
    def add_goal(self, goal):
        self.db.add_goal(
            goal.name,
            goal.target_amount,
            goal.deadline
        )

    # Remove goal
    def remove_goal(self, goal_name):
        self.db.remove_goal(goal_name)

    # Get all goals
    def get_all_goals(self):
        return self.db.get_goals()

    # Get a single goal
    def get_goal(self, goal_name):
        return self.db.find_goal(goal_name)