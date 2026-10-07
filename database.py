import psycopg2
import os
from dotenv import load_dotenv  
load_dotenv() 
def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
from datetime import date





def add_expense_to_db(amount, category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category) VALUES (%s, %s)",
        (amount, category)
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_expenses_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, category, date FROM expenses ORDER BY id DESC")
    expenses = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return expenses


def add_income_to_db(amount, source):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO income (amount, source) VALUES (%s, %s)",
        (amount, source)
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_income_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, source, date FROM income ORDER BY id DESC")
    income = cursor.fetchall()

    cursor.close()
    connection.close()
    return income


def add_budget_to_db(amount, category):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO budget (amount, category) VALUES (%s, %s)",
        (amount, category)
    )

    connection.commit()
    cursor.close()
    connection.close()


def get_budget_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, category, date FROM budget ORDER BY id DESC")
    budget = cursor.fetchall()

    cursor.close()
    connection.close()
    return budget


def get_balance_from_db():
    connection = get_connection()
    cursor = connection.cursor()

    # Get total income
    cursor.execute("SELECT SUM(amount) FROM income")
    total_income = cursor.fetchone()[0] or 0

    # Get total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses
    cursor.close()
    connection.close()

    return total_income, total_expenses, balance


