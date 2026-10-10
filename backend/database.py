
import sqlite3
import os

DATABASE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "campusconnect.db")

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Issues Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open'
        )
    """)
    
    # Create Users Table
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

def init_db():
    create_tables()

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully!")