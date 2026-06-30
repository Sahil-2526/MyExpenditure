class Transaction:
    def __init__ (self, date, amount, type, category, note):
        self.date = date
        self.amount = amount
        self.type = type
        self.category = category
        self.note = note

    def __repr__ (self):
        return f"[ {self.date} | {self.amount} | {self.type} | {self.category} | {self.note} ]"
    # used to represent how the data of the object will actually look if we use " print(object) "