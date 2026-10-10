
import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection, create_table


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()


def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


create_users_table()


@app.get("/")
def home():
    return {"message": "CampusConnect backend is running"}


@app.post("/register")
def register(data: dict):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        raise HTTPException(status_code=400, detail="Name, email, and password are required")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return {"message": "User registered successfully!"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    finally:
        conn.close()


@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return {
            "message": "Login successful!",
            "user_id": user[0],
            "name": user[1],
            "email": user[2]
        }
    finally:
        conn.close()



@app.post("/issues")
def create_issue(issue: dict):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO issues (title, category, location, description)
            VALUES (?, ?, ?, ?)
            """,
            (
                issue["title"],
                issue["category"],
                issue["location"],
                issue["description"]
            )
        )
        conn.commit()

        return {
            "message": "Issue created successfully",
            "issue_id": cursor.lastrowid
        }
    except KeyError as e:
        raise HTTPException(status_code=422, detail=f"Missing field: {e}")
    finally:
        conn.close()

@app.get("/issues")
def get_issues():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM issues ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@app.get("/issues")
def get_issues():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM issues ORDER BY id DESC")
        rows = cursor.fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "category": row["category"],
                "location": row["location"],
                "description": row["description"],
                "status": row["status"]
            }
            for row in rows
        ]
    finally:
        conn.close()

@app.get("/issues/{issue_id}")
def get_issue(issue_id: int):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
        issue = cursor.fetchone()

        if issue is None:
            raise HTTPException(status_code=404, detail="Issue not found")

        return dict(issue)
    finally:
        conn.close()


@app.put("/issues/{issue_id}/status")
def update_issue_status(issue_id: int, data: dict):
    status = data.get("status")

    if status not in ["Open", "In Progress", "Resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE issues SET status = ? WHERE id = ?",
            (status, issue_id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Issue not found")

        return {"message": "Status updated successfully"}
    finally:
        conn.close()

