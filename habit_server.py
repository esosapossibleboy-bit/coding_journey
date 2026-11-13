
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from habit_db import init_habit_db, create_habit, complete_habit

app = FastAPI(title="Esosa's Mobile Habit & Streak API")
HABIT_DB = "habits.db"


class NewHabitRequest(BaseModel):
    name: str


def fetch_habits_list(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, streak, last_completed FROM habits")
    rows = cursor.fetchall()
    return [
        {"id": r[0], "name": r[1], "streak": r[2], "last_completed": r[3]}
        for r in rows
    ]


@app.get("/habits")
def api_get_habits():
    conn = sqlite3.connect(HABIT_DB)
    init_habit_db(conn)

    habits = fetch_habits_list(conn)
    conn.close()

    return {"habits": habits}


@app.post("/habits")
def api_create_habit(req: NewHabitRequest):
    conn = sqlite3.connect(HABIT_DB)
    init_habit_db(conn)

    try:
        create_habit(conn, req.name)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Habit already exists"
        )

    habits = fetch_habits_list(conn)
    conn.close()

    return {"habits": habits}


@app.post("/habits/{habit_id}/complete")
def api_complete_habit(habit_id: int, today: str = None):
    conn = sqlite3.connect(HABIT_DB)
    init_habit_db(conn)

    new_streak = complete_habit(conn, habit_id, today)

    if new_streak is None:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Habit not found"
        )

    habits = fetch_habits_list(conn)
    conn.close()

    return {
        "streak": new_streak,
        "habits": habits
    }
