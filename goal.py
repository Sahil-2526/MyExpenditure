class Goal:
    def __init__(self, name, target_amount, deadline = None):
        self.name = name
        self.target_amount = target_amount
        self.deadline = deadline
    def __repr__(self):
        return (
            f"{self.name} | "
            f"Target : ₹{self.target_amount}"
        )