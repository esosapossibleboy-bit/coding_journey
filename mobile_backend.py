import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
from leaderboard_db import setup_database, save_score, get_all_scores

app = FastAPI()
DB_NAME = "mobile_game.db"


class ScoreSubmission(BaseModel):
    player: str
    points: int


@app.post("/scores")
def submit_score(submission: ScoreSubmission):
    conn = sqlite3.connect(DB_NAME)
    setup_database(conn)
    save_score(conn, submission.player, submission.points)
    conn.close()
    return {"status": "saved", "player": submission.player}


@app.get("/scores")
def fetch_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    setup_database(conn)
    rows = get_all_scores(conn)
    conn.close()
    return {"leaderboard": rows}
