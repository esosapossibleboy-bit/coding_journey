import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

from ai_mood import detect_mood
from ai_chatbot import ask_ai
from game_engine import move_player
from leaderboard_db import setup_database, save_score, get_all_scores

app = FastAPI(title="Esosa's Software Engineering Capstone")
CAPSTONE_DB = "capstone.db"


class MoveRequest(BaseModel):
    x: int
    y: int
    direction: str
    map_size: int = 5


@app.get("/ai/chat")
def smart_assistant(message: str):
    mood = detect_mood(message)
    reply = ask_ai(message)
    return {"mood": mood, "reply": reply}


@app.post("/game/move")
def game_step(move: MoveRequest):
    new_x, new_y = move_player(move.x, move.y, move.direction, move.map_size)
    return {"x": new_x, "y": new_y}


@app.post("/game/score")
def record_win(player: str, points: int):
    conn = sqlite3.connect(CAPSTONE_DB)
    try:
        setup_database(conn)
        save_score(conn, player, points)
        top_scores = get_all_scores(conn)
    finally:
        conn.close()
    return {"leaderboard": top_scores}
