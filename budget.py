class Budget:
    def __init__(self, category, limit_count, month, year):
        self.category = category
        self.limit_count = limit_count
        self.month = month
        self.year = year
    def __repr__(self):
        return (
            f"{self.category.name} | "
            f"₹{self.limit_amount} | "
            f"{self.month}/{self.year}"
        )