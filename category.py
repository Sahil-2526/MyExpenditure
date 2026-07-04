from enums import TransactionType

class Category:
    def __init__(self, name, transaction_type: TransactionType, is_default=False):
        self.name = name
        self.transaction_type = transaction_type
        self.is_default = is_default

    def __repr__(self):
        return (
            f"{self.name} "
            f"({self.transaction_type.value}) "
            f"- Default: {self.is_default}"
        )