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

# 
def add_issue_owner_column():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA table_info(issues)")
        columns = [row["name"] for row in cursor.fetchall()]

        if "user_id" not in columns:
            cursor.execute(
                "ALTER TABLE issues ADD COLUMN user_id INTEGER"
            )
            conn.commit()
    finally:
        conn.close()


add_issue_owner_column()
# 


# @app.get("/")
# def home():
#     return {"message": "CampusConnect backend is running"}


# @app.post("/register")
# def register(data: dict):
#     name = data.get("name")
#     email = data.get("email")
#     password = data.get("password")

#     if not name or not email or not password:
#         raise HTTPException(
#             status_code=400,
#             detail="Name, email, and password are required"
#         )

#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute(
#             "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
#             (name, email, password)
#         )
#         conn.commit()
#         return {"message": "User registered successfully!"}
#     except sqlite3.IntegrityError:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already registered"
#         )
#     finally:
#         conn.close()


# tie rollnumber to email
@app.post("/register")
def register(data: dict):
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Username, email, and password are required"
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE name = ?",
            (name,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="This username or email is already registered."
            )

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=409,
                detail="This email is already registered."
            )

        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password)
        )

        conn.commit()

        return {
            "message": "User registered successfully!"
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="This username or email is already registered."
        )

    finally:
        conn.close()

# tie rollnumber to email



@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=400,
            detail="Email and password are required"
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return {
            "message": "Login successful!",
            "user_id": user[0],
            "name": user[1],
            "email": user[2]
        }
    finally:
        conn.close()
# @app.get("/issues")
# def get_issues():
#     conn = get_connection()
#     cursor = conn.cursor()
#     try:
#         cursor.execute("SELECT * FROM issues ORDER BY id DESC")
#         rows = cursor.fetchall()
#         return [dict(row) for row in rows]
#     finally:
#         conn.close()

# 
@app.get("/issues")
def get_issues(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT * FROM issues
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    finally:
        conn.close()
# 

@app.get("/issues/{issue_id}")
def get_issue(issue_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
        row = cursor.fetchone()

        if row is None:
            raise HTTPException(status_code=404, detail="Issue not found")

        return dict(row)
    finally:
        conn.close()



# @app.post("/issues")
# def create_issue(issue: dict):
#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         cursor.execute(
#             """
#             INSERT INTO issues (title, category, location, description)
#             VALUES (?, ?, ?, ?)
#             """,
#             (
#                 issue["title"],
#                 issue["category"],
#                 issue["location"],
#                 issue["description"]
#              )
#         )
        
#         conn.commit()
#         issue_id = cursor.lastrowid

#         return {
#             "message": "Issue created successfully",
#             "issue_id": issue_id
#         }
#     finally:
#         conn.close()


# 
@app.post("/issues")
def create_issue(issue: dict):
    user_id = issue.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="User ID is required"
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check that the user exists
        cursor.execute(
            "SELECT id FROM users WHERE id = ?",
            (user_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid user"
            )

        required_fields = [
            "title", "category", "location", "description"
        ]

        if any(not issue.get(field) for field in required_fields):
            raise HTTPException(
                status_code=400,
                detail="All issue fields are required"
            )

        cursor.execute(
            """
            INSERT INTO issues
                (title, category, location, description, user_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                issue["title"],
                issue["category"],
                issue["location"],
                issue["description"],
                user_id
            )
        )

        conn.commit()

        return {
            "message": "Issue created successfully",
            "issue_id": cursor.lastrowid
        }

    finally:
        conn.close()
# 
    
@app.put("/issues/{issue_id}/status")
def update_issue_status(issue_id: int, data: dict):
    status = data.get("status")

    if status not in ["Open", "In Progress", "Resolved"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM issues WHERE id = ?",
            (issue_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail="Issue not found"
            )

        cursor.execute(
            "UPDATE issues SET status = ? WHERE id = ?",
            (status, issue_id)
        )

        conn.commit()

        return {
            "message": "Status updated successfully",
            "issue_id": issue_id,
            "status": status
        }
    finally:
        conn.close()
    





