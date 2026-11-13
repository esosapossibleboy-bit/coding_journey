import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
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
        {
            "id": habit_id,
            "name": name,
            "streak": streak,
            "last_completed": last_completed,
        }
        for habit_id, name, streak, last_completed in rows
    ]

@app.get("/", response_class=HTMLResponse)
def mobile_habit_preview():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8" /><title>Mobile Habit & Streak App</title></head>
    <body style="background:#11111b; color:white; font-family:sans-serif; display:flex; justify-content:center; padding:30px;">
        <div style="width:360px; min-height:640px; background:#1e1e2e; border:4px solid #89b4fa; border-radius:28px; padding:24px;">
            <h2>🔥 Daily Habit Tracker</h2>
            <div style="display:flex; gap:8px; margin-bottom:20px;">
                <input id="habitInput" placeholder="New habit name..." style="flex:1; padding:10px; border-radius:8px; border:none;" />
                <button onclick="addHabit()" style="padding:10px 14px; background:#a6e3a1; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Add</button>
            </div>
            <div id="habitList"></div>
        </div>

        <script>
            async function loadHabits() {
                const res = await fetch("/habits");
                const data = await res.json();
                renderHabits(data.habits);
            }

            async function addHabit() {
                const input = document.getElementById("habitInput");
                if (!input.value.trim()) return;
                const res = await fetch("/habits", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ name: input.value })
                });
                const data = await res.json();
                input.value = "";
                renderHabits(data.habits);
            }

            async function completeHabit(id) {
                const res = await fetch(`/habits/${id}/complete`, { method: "POST" });
                const data = await res.json();
                renderHabits(data.habits);
            }

            function renderHabits(habits) {
                const list = document.getElementById("habitList");
                list.innerHTML = habits.map(h => `
                    <div style="background:#11111b; padding:14px; border-radius:12px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight:bold;">${h.name}</div>
                            <div style="color:#f9e2af; font-size:14px;">🔥 ${h.streak} day streak</div>
                        </div>
                        <button onclick="completeHabit(${h.id})" style="padding:8px 12px; background:#89b4fa; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Done</button>
                    </div>
                `).join("");
            }

            loadHabits();
        </script>
    </body>
    </html>
    """

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
        raise HTTPException(status_code=400, detail="Habit already exists")
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
        raise HTTPException(status_code=404, detail="Habit not found")
    habits = fetch_habits_list(conn)
    conn.close()
    return {"streak": new_streak, "habits": habits}
