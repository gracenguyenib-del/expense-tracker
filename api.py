from fastapi import FastAPI
from database import get_connection

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Expense Tracker API is running."}
@app.get("/income")
def get_income():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, source, date FROM income ORDER BY id DESC")
    income = cursor.fetchall()

    cursor.close()
    connection.close()
    return {"income": income}
@app.post("/income")
def add_income(amount: float, source: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO income (amount, source) VALUES (%s, %s)",
        (amount, source)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"Income of {amount} from {source} added successfully."}
@app.get("/expenses")
def get_expenses():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, category, date FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()
    return {"expenses": expenses}
@app.post("/expenses")
def add_expense(amount: float, category: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (%s, %s)",
        (amount, category)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"Expense of {amount} for {category} added successfully."}
@app.get("/budget")
def get_budget():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, category FROM budget ORDER BY id DESC")
    budget = cursor.fetchall()

    cursor.close()
    connection.close()
    return {"budget": budget}
@app.post("/budget")
def add_budget(amount: float, category: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO budget (amount, category) VALUES (%s, %s)",
        (amount, category)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"Budget of {amount} for {category} added successfully."}
@app.get("/balance")
def get_balance():
    connection = get_connection()
    cursor = connection.cursor()

    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses

    cursor.close()
    connection.close()

    return {"total_income": total_income, "total_expenses": total_expenses, "balance": balance}
@app.get("/transactions")
def view_transactions():
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch income records
    cursor.execute("SELECT id, amount, source, date FROM income ORDER BY id DESC")
    income = cursor.fetchall()

    # Fetch expense records
    cursor.execute("SELECT id, amount, category, date FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return {"income": income, "expenses": expenses}
@app.get("/spending_summary")
def spending_summary():
    connection = get_connection()
    cursor = connection.cursor()

    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses

    cursor.close()
    connection.close()

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance
    }
@app.get("/financial_health")
def financial_health():
    connection = get_connection()
    cursor = connection.cursor()

    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses

    # Determine financial health status
    if balance > 0:
        status = "Good"
    elif balance == 0:
        status = "Neutral"
    else:
        status = "Poor"

    cursor.close()
    connection.close()

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "financial_health_status": status
    }