
import sqlite3

def create_database():

    conn = sqlite3.connect("students.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            english INTEGER,
            python INTEGER,
            maths INTEGER,
            dbms INTEGER,
            java INTEGER,
            total INTEGER,
            percentage REAL,
            grade TEXT,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


create_database()
