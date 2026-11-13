import sqlite3
from datetime import date, timedelta

def init_habit_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            streak INTEGER DEFAULT 0,
            last_completed TEXT
        )
    """)
    conn.commit()


def create_habit(conn, name):
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO habits (name, streak, last_completed) VALUES (?, ?, ?)",
        (name, 0, None)
    )

    conn.commit()
    return cursor.lastrowid


def complete_habit(conn, habit_id, today_str=None):
    # Default to today's date
    if today_str is None:
        today_str = date.today().isoformat()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT streak, last_completed FROM habits WHERE id = ?",
        (habit_id,)
    )

    row = cursor.fetchone()

    if not row:
        return None

    current_streak, last_completed = row

    # Calculate yesterday's date
    yesterday_str = (
        date.fromisoformat(today_str) - timedelta(days=1)
    ).isoformat()

    # Calculate the new streak
    if last_completed == today_str:
        new_streak = current_streak
    elif last_completed == yesterday_str:
        new_streak = current_streak + 1
    else:
        new_streak = 1

    # Update the database
    cursor.execute(
        """
        UPDATE habits
        SET streak = ?, last_completed = ?
        WHERE id = ?
        """,
        (new_streak, today_str, habit_id)
    )

    conn.commit()

    return new_streak