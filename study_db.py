import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_study_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            content TEXT
        )
    """)
    conn.commit()

def register_user(conn, username, password):
    hashed = hash_password(password)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hashed),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None

def verify_user(conn, username, password):
    hashed = hash_password(password)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE username = ? AND password_hash = ?",
        (username, hashed),
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

def add_study_note(conn, user_id, title, content):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
        (user_id, title, content),
    )
    conn.commit()

def get_user_notes(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT title, content FROM notes WHERE user_id = ?",
        (user_id,),
    )
    return cursor.fetchall()
