from enums import TransactionType
class Transaction:
    def __init__ (self, date, amount, transaction_type: TransactionType, category, note):
        self.date = date
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category
        self.note = note

    def __repr__ (self):
        return f"[ {self.date} | {self.amount} | {self.transaction_type} | {self.category} | {self.note} ]"
    # used to represent how the data of the object will actually look if we use " print(object) "