from fastapi import FastAPI, Depends, HTTPException
from database import get_connection
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
app = FastAPI()
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()  
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import(get_monthly_income_expenses_budget)


password_hash = PasswordHash.recommended()
import os
JWT_SECRET = os.getenv("JWT_SECRET")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
def create_access_token(user_id):
    payload = {
        "sub":str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

class IncomeCreate(BaseModel):
    amount: float = Field(gt=0)
    source: str=Field(min_length=1, max_length=100)

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)

class BudgetCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=100)

class UserCreate(BaseModel):
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=100)
    password: str = Field(min_length=8, max_length=100)

@app.post("/register")
def register_user(user: UserCreate):
    connection = get_connection()
    cursor = connection.cursor()

    
    hashed_password = password_hash.hash(user.password)

    cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (user.email, hashed_password)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"User with email {user.email} registered successfully."}

@app.post("/login")
def login_user(user: OAuth2PasswordRequestForm = Depends()):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE email = %s",
        (user.username,)
    )
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    user_id=result[0]
    stored_hashed_password = result[1]

    if password_hash.verify(user.password, stored_hashed_password):
        access_token = create_access_token(user_id)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password.")





@app.get("/")
def home():
    return {"message": "Expense Tracker API is running."}
@app.get("/income")
def get_income(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, source, date FROM income WHERE user_id = %s", (user_id,))
    income = cursor.fetchall()

    cursor.close()
    connection.close()
    return {"income": income}
@app.post("/income")
def add_income(income: IncomeCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO income (amount, source, user_id) VALUES (%s, %s, %s)",
        (income.amount, income.source, user_id)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"Income of {income.amount} from {income.source} added successfully."}
@app.get("/expenses")
def get_expenses(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, category, date FROM expenses WHERE user_id = %s", (user_id,))
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()
    return {"expenses": expenses}
@app.post("/expenses")
def add_expense(expense: ExpenseCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO expenses (amount, category, user_id) VALUES (%s, %s, %s)",
        (expense.amount, expense.category, user_id)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"Expense of {expense.amount} for {expense.category} added successfully."}
@app.get("/budget")
def get_budget(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, amount, category FROM budget WHERE user_id = %s", (user_id,))
    budget = cursor.fetchall()

    cursor.close()
    connection.close()
    return {"budget": budget}
@app.post("/budget")
def add_budget(budget: BudgetCreate, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO budget (amount, category, user_id) VALUES (%s, %s, %s)",
        (budget.amount, budget.category, user_id)
    )

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"Budget of {budget.amount} for {budget.category} added successfully."}
@app.get("/balance")
def get_balance(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM income WHERE user_id = %s", (user_id,))
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (user_id,))
    total_expenses = cursor.fetchone()[0] or 0

    # Calculate balance
    balance = total_income - total_expenses

    cursor.close()
    connection.close()

    return {"total_income": total_income, "total_expenses": total_expenses, "balance": balance}
@app.get("/transactions")
def view_transactions(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    # Fetch income records
    cursor.execute("SELECT id, amount, source, date FROM income WHERE user_id = %s", (user_id,))
    income = cursor.fetchall()


    cursor.execute("SELECT id, amount, category, date FROM expenses WHERE user_id = %s", (user_id,))
    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return {"income": income, "expenses": expenses}
@app.get("/spending_summary")
def spending_summary(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    # Calculate total income
    cursor.execute("SELECT SUM(amount) FROM income WHERE user_id = %s", (user_id,))
    total_income = cursor.fetchone()[0] or 0

    # Calculate total expenses
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (user_id,))
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
def financial_health(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    connection = get_connection()
    cursor = connection.cursor()

    
    cursor.execute("SELECT SUM(amount) FROM income WHERE user_id = %s", (user_id,))
    total_income = cursor.fetchone()[0] or 0

    
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE user_id = %s", (user_id,))
    total_expenses = cursor.fetchone()[0] or 0

    
    balance = total_income - total_expenses

    
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
@app.get("/monthly_summary")
def monthly_summary(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    monthly_income, monthly_expenses, monthly_budget = get_monthly_income_expenses_budget()

    return {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "monthly_budget": monthly_budget
    }