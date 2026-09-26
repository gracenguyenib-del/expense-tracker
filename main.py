print('================================')
print('M-PESA MONEYMAP')
print('================================')

from datetime import datetime
transaction=[]
monthly_budget=0
def get_date():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def add_income():
    amount = float(input("Enter income amount: "))
    source = input("Enter income source: ")
    date = get_date()
    transaction.append({"type": "income", "amount": amount, "source": source, "date": date})
    print(f"Income of {amount} from {source} added on {date}.")
def add_expense():
    amount = float(input("Enter expense amount: "))
    category = input("Enter expense category: ")
    date = get_date()
    transaction.append({"type": "expense", "amount": amount, "category": category, "date": date})
    print(f"Expense of {amount} for {category} added on {date}.")
def view_transactions():
    if not transaction:
        print("No transactions recorded.")
        return
    print("Transactions:")
    for t in transaction:
        if t["type"] == "income":
            print(f"Income: {t['amount']} from {t['source']} on {t['date']}")
        else:
            print(f"Expense: {t['amount']} for {t['category']} on {t['date']}")
def calculate_balance():
    balance = 0
    for t in transaction:
        if t["type"] == "income":
            balance += t["amount"]
        else:
            balance -= t["amount"]
    print(f"Current balance: {balance}") 
def set_budget():
    global monthly_budget
    monthly_budget = float(input("Enter your monthly budget: "))
    print(f"Monthly budget set to {monthly_budget}.")
def spending_summary():
    total_expenses = sum(t["amount"] for t in transaction if t["type"] == "expense")
    print(f"Total expenses: {total_expenses}")
    if monthly_budget > 0:
        print(f"Budget remaining: {monthly_budget - total_expenses}")
    else:
        print("No budget set.")
def financial_health():
    total_income = sum(t["amount"] for t in transaction if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transaction if t["type"] == "expense")
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
    
    if choice == '1':
        add_income()
    elif choice == '2':
        add_expense()
    elif choice == '3':
        view_transactions()
    elif choice == '4':
        calculate_balance()
    elif choice == '5':
        set_budget()
    elif choice == '6':
        spending_summary()
    elif choice == '7':
        financial_health()
    elif choice == '8':
        print("Exiting M-PESA MONEYMAP. Goodbye!")
        break
    else:
        print("Invalid option. Please try again.")