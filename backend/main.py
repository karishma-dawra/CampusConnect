from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection, create_table
from models import IssueCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()

@app.get("/")
def home():
    return {"message": "CampusConnect backend is running"}

@app.post("/issues")
def create_issue(issue: IssueCreate):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO issues (title, category, location, description, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        issue.title,
        issue.category,
        issue.location,
        issue.description,
        "Open"
    ))

    connection.commit()
    issue_id = cursor.lastrowid
    connection.close()

    return {
        "message": "Issue created successfully",
        "id": issue_id,
        "status": "Open"
    }

@app.get("/issues")
def get_issues():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, category, location, description, status
        FROM issues
    """)

    rows = cursor.fetchall()
    connection.close()

    issues = []

    for row in rows:
        issues.append({
            "id": row[0],
            "title": row[1],
            "category": row[2],
            "location": row[3],
            "description": row[4],
            "status": row[5]
        })

    return issues

@app.get("/issues/{issue_id}")
def get_issue(issue_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, category, location, description, status
        FROM issues
        WHERE id = ?
    """, (issue_id,))

    row = cursor.fetchone()
    connection.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Issue not found")

    return {
        "id": row[0],
        "title": row[1],
        "category": row[2],
        "location": row[3],
        "description": row[4],
        "status": row[5]
    }

@app.put("/issues/{issue_id}/status")
def update_status(issue_id: int, status: dict):
    new_status = status.get("status")

    if new_status not in ["Open", "In Progress", "Resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE issues
        SET status = ?
        WHERE id = ?
    """, (new_status, issue_id))

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Issue not found")

    connection.commit()
    connection.close()

    return {
        "message": "Issue status updated successfully",
        "id": issue_id,
        "status": new_status
    }
