from enums import CategoryType
class Transaction:
    def __init__ (self, date, amount, category_type: CategoryType, category, note):
        self.date = date
        self.amount = amount
        self.category_type = category_type
        self.category = category
        self.note = note

    def __repr__ (self):
        return f"[ {self.date} | {self.amount} | {self.category_type} | {self.category} | {self.note} ]"
    # used to represent how the data of the object will actually look if we use " print(object) "