from enums import TransactionType

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.categories = []
        self.budgets = []
        self.goals = []
    
    # ----------------------- Transaction Functions -------------------------------------------------------
    # Add transaction 
    def add_transaction(self,transaction):
        self.transactions.append(transaction)

    # View all transaction
    def get_all_transactions(self):
        return self.transactions
    
    # Get single transaction 
    def get_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    
    # Calculate total_credit
    def total_credit(self):
        return sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.CREDIT)

    # Calculate total_debit
    def total_debit(self):
        return sum(t.amount for t in self.transactions if t.transaction_type == TransactionType.DEBIT)
    
    # calculate balance
    def balance(self):
        return self.total_credit() - self.total_debit()
    
    # category wise spending
    def category_wise_spending(self):
        summary = {}
        for t in self.transactions:
            if t.transaction_type == TransactionType.DEBIT:
                summary[t.category.name] = summary.get(t.category, 0) + t.amount
        return summary
    
    # Get transaction by date
    def transaction_by_date(self, day, month, year):
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
    
    # Edit transaction 
    def edit_transaction(self, transaction_id, amount = None, date = None, transaction_type = None, category = None, note = None ):
        transaction = self.find_transaction(transaction_id)
        if transaction is None:
            print(f"Transaction with ID {transaction_id} not found.")
            return
        if amount is not None:
            transaction.amount = amount
        if date is not None:
            transaction.date = date
        if transaction_type is not None:
            transaction.transaction_type = transaction_type
        if category is not None:
            transaction.category = category
        if note is not None:
            transaction.note = note
        print(f"Transaction {transaction_id} updated successfully.")

    # ---------------------------Category Functions----------------------------------------------------------
    # Add category
    def add_category(self, category):
        for prev_cat in self.categories:
            if prev_cat.name.lower() == category.name.lower():
                print(f"Category '{category.name}' already exist. ")
                return
        self.categories.append(category)
        print(f"Category '{category.name}' added successfully. ")

    # Remove category
    def remove_category(self, category_name):
        for category in self.categories:
            if category.name.lower() == category_name.lower():
                self.categories.remove(category)
                print(f"Category '{category_name}' removed successfully.")
                return
        print(f"Category '{category_name}' not found.")
    
    # Get all categories
    def get_all_categories(self):
        return self.categories
    
    # Get single transaction
    def find_category(self, category_name):
        for category in self.categories:
            if category.name.lower() == category_name.lower():
                return category
        return None 
    
    # ------------------------------Budget Functions--------------------------------------------------------------
    # Add budget
    def add_budget(self, budget):
        for existing_budget in self.budgets:
            if (
                existing_budget.category.name.lower() == budget.category.name.lower()
                and existing_budget.month == budget.month
                and existing_budget.year == budget.year
            ):
                print(
                    f"Budget for {budget.category.name} "
                    f"({budget.month}/{budget.year}) already exists."
                )
                return
        self.budgets.append(budget)
        print(f"Budget added for {budget.category.name}.")

    # Remove Budget
    def remove_budget(self, category_name, month, year):
        for budget in self.budgets:
            if (
                budget.category.name.lower() == category_name.lower()
                and budget.month == month
                and budget.year == year
            ):
                self.budgets.remove(budget)
                print(f"Budget removed for {category_name}.")
                return
        print("Budget not found.")

    # Get all budgets
    def get_all_budgets(self):
        return self.budgets

    # Get budget by name and month of a year
    def get_budget(self, category_name, month, year):
        for budget in self.budgets:
            if (
                budget.category.name.lower() == category_name.lower()
                and budget.month == month
                and budget.year == year
            ):
                return budget
        return None
    
    # Summarize a budget in detail 
    def check_budget(self, category_name, month, year):
        budget = self.get_budget(category_name, month, year)
        if budget is None:
            print("Budget not found.")
            return
        spent = 0
        for transaction in self.transactions:
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


    # -------------------------------------Goal functions--------------------------------------------------
    # Add goal
    def add_goal(self, goal):
        for existing_goal in self.goals:
            if existing_goal.name.lower() == goal.name.lower():
                print(f"Goal '{goal.name}' already exists.")
                return
        self.goals.append(goal)
        print(f"Goal '{goal.name}' added successfully.")

    # Remove goal
    def remove_goal(self, goal_name):
        for goal in self.goals:
            if goal.name.lower() == goal_name.lower():
                self.goals.remove(goal)
                print(f"Goal '{goal_name}' removed successfully.")
                return
        print(f"Goal '{goal_name}' not found.")

    # Get all goals
    def get_all_goals(self):
        return self.goals

    # Get a single goal
    def get_goal(self, goal_name):
        for goal in self.goals:
            if goal.name.lower() == goal_name.lower():
                return goal
        return None