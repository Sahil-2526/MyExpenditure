from enums import TransactionType

class Transaction:
    def __init__(self, uid, date, amount, transaction_type: TransactionType, category, note):
        self.uid = uid
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.note = note

    def __repr__(self):
        return f"[ {self.date} | ₹{self.amount} | {self.transaction_type.value} | {self.category} | {self.note} ]"