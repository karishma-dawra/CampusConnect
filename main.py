import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = (
        sqlite3.Row
    ) 
    return conn

# Request format for Register
class RegisterData(BaseModel):
    name: str
    email: str
    password: str

# Request format for Login
class LoginData(BaseModel):
    email: str
    password: str

# ---------------- 1. REGISTER ROUTE ----------------
@app.post("/register")
def register(data: RegisterData):
    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    # Insert user into database
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (data.name, data.email, data.password),
    )

    conn.commit()
    conn.close()

    return {"message": "User registered successfully!"}

# ---------------- 2. LOGIN ROUTE ----------------
@app.post("/login")
def login(data: LoginData):
    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    # Search for matching user
    cursor.execute(
        "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
        (data.email, data.password),
    )
    user = cursor.fetchone()  # Returns a tuple like (1, "Alice", "alice@test.com") or None

    conn.close()

    # Check if user was found
    if user:
        return {
            "message": "Login successful!",
            "user_id": user[0],
            "name": user[1],
            "email": user[2],
        }
    else:
        return {"message": "Invalid email or password"}