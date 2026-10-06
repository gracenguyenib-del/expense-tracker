print("================================")
print("M-PESA MONEYMAP")
print("================================")

from datetime import date

from database import (
    add_income_to_db,
    add_expense_to_db,
    add_budget_to_db,
    get_balance_from_db,
    get_expenses_from_db,
    get_income_from_db,
    get_budget_from_db
)


def add_income():
    try:
        amount = float(input("Enter income amount: "))
        source = input("Enter income source: ")

        add_income_to_db(amount, source)

        print(f"Income of {amount} from {source} added successfully.")

    except ValueError:
        print("Invalid amount. Please enter a number.")


def add_expense():
    try:
        amount = float(input("Enter expense amount: "))
        category = input("Enter expense category: ")

        add_expense_to_db(amount, category)

        print(f"Expense of {amount} for {category} added successfully.")

    except ValueError:
        print("Invalid amount. Please enter a number.")


def view_transactions():
    income = get_income_from_db()
    expenses = get_expenses_from_db()

    print("\n--- INCOME ---")

    if income:
        for i in income:
            print(f"Income: {i[1]} from {i[2]}")
    else:
        print("No income records found.")

    print("\n--- EXPENSES ---")

    if expenses:
        for e in expenses:
            print(f"Expense: {e[1]} for {e[2]}")
    else:
        print("No expense records found.")


def calculate_balance():
    income, expenses, balance = get_balance_from_db()

    print("\n--- FINANCIAL BALANCE ---")
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Current Balance: {balance}")


def set_budget():
    try:
        amount = float(input("Enter your monthly budget: "))
        category = input("Enter budget category: ")

        add_budget_to_db(amount, category)

        print(f"Budget of {amount} for {category} added successfully.")

    except ValueError:
        print("Invalid amount. Please enter a number.")


def spending_summary():
    expenses = get_expenses_from_db()
    budgets = get_budget_from_db()

    total_expenses = sum(e[1] for e in expenses)

    print("\n--- SPENDING SUMMARY ---")
    print(f"Total expenses: {total_expenses}")

    if budgets:
        total_budget = sum(b[1] for b in budgets)
        remaining = total_budget - total_expenses

        print(f"Total budget: {total_budget}")
        print(f"Budget remaining: {remaining}")
    else:
        print("No budget has been set.")


def financial_health():
    income = get_income_from_db()
    expenses = get_expenses_from_db()

    total_income = sum(i[1] for i in income)
    total_expenses = sum(e[1] for e in expenses)

    print("\n--- FINANCIAL HEALTH ---")

    if total_income > total_expenses:
        print("You are in good financial health.")
    elif total_income < total_expenses:
        print("You are overspending. Consider reviewing your expenses.")
    else:
        print("Your income and expenses are balanced.")


while True:
    print("\nMenu:")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Calculate Balance")
    print("5. Set Monthly Budget")
    print("6. Spending Summary")
    print("7. Financial Health Check")
    print("8. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_income()

    elif choice == "2":
        add_expense()

    elif choice == "3":
        view_transactions()

    elif choice == "4":
        calculate_balance()

    elif choice == "5":
        set_budget()

    elif choice == "6":
        spending_summary()

    elif choice == "7":
        financial_health()

    elif choice == "8":
        print("Exiting M-PESA MONEYMAP. Goodbye!")
        break

    else:
        print("Invalid option. Please try again.")
