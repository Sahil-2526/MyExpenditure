from enums import TransactionType

class FinanceManager:
    def __init__(self, db):
        self.db = db
    
    # ----------------------- Transaction Functions -----------------------
    def add_transaction(self, transaction):
        self.db.add_transaction(
            transaction.amount,
            transaction.date.isoformat(),
            transaction.transaction_type.value,
            transaction.category.id,
            transaction.note
        )

    def get_all_transactions(self):
        return self.db.get_transactions()
    
    def get_transaction(self, transaction_id):
        return self.db.find_transaction(transaction_id)
    
    def total_credit(self):
        transactions = self.db.get_transactions()
        # Tuple index 1 is amount, index 3 is transaction_type
        return sum(t[1] for t in transactions if t[3] == TransactionType.CREDIT.value)

    def total_debit(self):
        transactions = self.db.get_transactions()
        return sum(t[1] for t in transactions if t[3] == TransactionType.DEBIT.value)
    
    def balance(self):
        return self.total_credit() - self.total_debit()
    
    def category_wise_spending(self):
        transactions = self.db.get_transactions()
        categories = self.get_all_categories()
        cat_map = {c[0]: c[1] for c in categories}
        summary = {}
        for t in transactions:
            if t[3] == TransactionType.DEBIT.value:
                cat_name = cat_map.get(t[4], "Uncategorized")
                summary[cat_name] = summary.get(cat_name, 0) + t[1]
        return summary
    
    def edit_transaction(
        self,
        transaction_id,
        amount=None,
        date=None,
        transaction_type=None,
        category_id=None,
        note=None
    ):
        self.db.update_transaction(
            transaction_id,
            amount,
            date.isoformat() if date else None,
            transaction_type.value if transaction_type else None,
            category_id,
            note
        )

    # --------------------------- Category Functions ---------------------------
    def add_category(self, category):
        self.db.add_category(
            category.name,
            category.transaction_type.value,
            category.is_default
        )

    def remove_category(self, category_name):
       self.db.remove_category(category_name)
    
    def get_all_categories(self):
        return self.db.get_categories()
    
    def find_category(self, category_name):
        return self.db.find_category(category_name)
    
    # ------------------------------ Budget Functions ------------------------------
    def add_budget(self, budget):
        self.db.add_budget(
            budget.category.id,
            budget.limit_amount,
            budget.month,
            budget.year
        )
 
    def remove_budget(self, category_id, month, year):
        self.db.remove_budget(category_id, month, year)

    def get_all_budgets(self):
        return self.db.get_budgets()

    def get_budget(self, category_id, month, year):
       return self.db.find_budget(category_id, month, year)
    
    def check_budget(self, category_name, month, year):
        category = self.find_category(category_name)
        if category is None:
            return None
        
        # category[0] is id from tuple record
        budget = self.get_budget(category[0], month, year)
        if budget is None:
            return None
            
        spent = 0
        transactions = self.db.get_transactions()
        for transaction in transactions:
            # transaction[4] is category_id, transaction[2] is date string, transaction[1] is amount
            t_cat = self.db.find_transaction(transaction[0])
            # Check matching category ID, matching year/month from date, and DEBIT type
            if (
                transaction[4] == category[0]
                and int(transaction[2][5:7]) == month
                and int(transaction[2][:4]) == year
                and transaction[3] == TransactionType.DEBIT.value
            ):
                spent += transaction[1]

        limit_amount = budget[3] # budget tuple index 3 is limit_amount
        remaining = limit_amount - spent

        return {
            "category": category_name,
            "budget": limit_amount,
            "spent": spent,
            "remaining": remaining,
            "status": remaining >= 0
        }

    # ------------------------------------- Goal functions -------------------------------------
    def add_goal(self, goal):
        self.db.add_goal(
            goal.name,
            goal.target_amount,
            goal.deadline
        )

    def remove_goal(self, goal_name):
        self.db.remove_goal(goal_name)

    def get_all_goals(self):
        return self.db.get_goals()

    def get_goal(self, goal_name):
        return self.db.find_goal(goal_name)