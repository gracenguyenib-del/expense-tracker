from datetime import date
import sqlite3


def create_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL DEFAULT CURRENT_DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            date TEXT NOT NULL DEFAULT CURRENT_DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL DEFAULT CURRENT_DATE,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_expense_to_db(amount, category):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, date.today())
    )

    connection.commit()
    connection.close()


def get_expenses_from_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    connection.close()
    return expenses


def add_income_to_db(amount, source):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO income (amount, source, date) VALUES (?, ?, ?)",
        (amount, source, date.today())
    )

    connection.commit()
    connection.close()


def get_income_from_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM income")
    income = cursor.fetchall()

    connection.close()
    return income


def add_budget_to_db(amount, category):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO budget (amount, category, date) VALUES (?, ?, ?)",
        (amount, category, date.today())
    )

    connection.commit()
    connection.close()


def get_budget_from_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM budget")
    budget = cursor.fetchall()

    connection.close()
    return budget


def get_balance_from_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    # Get total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    # Get total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses

    connection.close()

    return total_income, total_expenses, balance
create_database()
