class Budget:
    def __init__(self, uid, category, limit_amount, month, year):
        self.uid = uid
        self.category = category
        self.limit_amount = limit_amount
        self.month = month
        self.year = year
        
    def __repr__(self):
        return (
            f"{self.category.name} | "
            f"₹{self.limit_amount} | "
            f"{self.month}/{self.year}"
        )