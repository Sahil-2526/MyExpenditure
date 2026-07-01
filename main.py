from finance import (
    add_transaction,
    view_transactions,
    total_credit,
    total_debit,
    balance,
    category_wise_spending
)

# Add sample data
add_transaction("2026-06-30", 50000, "Credit", "Salary", "June salary")
add_transaction("2026-06-30", 200, "Debit", "Food", "Lunch")
add_transaction("2026-06-30", 1000, "Debit", "Shopping", "Amazon")
add_transaction("2026-06-30", 500, "Debit", "Food", "Dinner")

# View transactions
print("\nALL TRANSACTIONS:")
for t in view_transactions():
    print(t)

# Financial summary
print("\nTOTAL INCOME:", total_credit())
print("TOTAL EXPENSE:", total_debit())
print("BALANCE:", balance())

# Category summary
print("\nCATEGORY BREAKDOWN:")
print(category_wise_spending())