from category import Category
from category_type import CategoryType

food = Category("Food", CategoryType.DEBIT, True)
salary = Category("Salary", CategoryType.CREDIT, True)
gaming = Category("Gaming", CategoryType.DEBIT)

print(food)
print(salary)
print(gaming)