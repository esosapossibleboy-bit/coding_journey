import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from leaderboard_db import setup_database, save_score, get_all_scores

app = FastAPI(title="Esosa's AI Arcade Arena")
ARCADE_DB = "arcade_arena.db"


class GameResult(BaseModel):
    player: str
    score: int


def generate_ai_commentary(score):
    if score >= 5:
        return "🔥 Legendary jump skills! Top tier!"
    else:
        return "🤖 Good warm-up! Tap Spacebar earlier next time!"


@app.post("/submit-score")
def submit_game_score(result: GameResult):
    # Connect to SQLite database
    conn = sqlite3.connect(ARCADE_DB)

    try:
        # Set up database tables
        setup_database(conn)

        # Save player's score
        save_score(conn, result.player, result.score)

        # Fetch leaderboard
        rows = get_all_scores(conn)

    finally:
        # Close database connection
        conn.close()

    # Generate AI commentary
    comment = generate_ai_commentary(result.score)

    # Return commentary and top 5 scores
    return {
        "ai_comment": comment,
        "leaderboard": rows[:5]
    }


@app.get("/", response_class=HTMLResponse)
def serve_arcade():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8" /><title>Esosa's AI Arcade Arena</title></head>
    <body style="background:#1e1e2e; color:white; font-family:sans-serif; text-align:center; padding:20px;">
        <h1>🕹️ Esosa's AI Arcade Arena</h1>
        <input id="playerName" value="Esosa" placeholder="Your Name" style="padding:8px; border-radius:6px;" />
        <h2 id="scoreText">Score: 0</h2>
        <canvas id="gameCanvas" width="600" height="300" style="background:#11111b; border:2px solid #89b4fa;"></canvas>
        <h3 id="aiBox" style="color:#a6e3a1;">🤖 AI Coach: Ready when you are!</h3>
        <h3>🏆 Live SQL Leaderboard</h3>
        <ul id="board" style="list-style:none; padding:0;"></ul>

        <script>
            const canvas = document.getElementById("gameCanvas");
            const ctx = canvas.getContext("2d");
            let y = 210, velocityY = 0, obstacleX = 600, score = 0, gameOver = false;
            const floorY = 210, gravity = 0.8;

            async function sendScoreToBackend(finalScore) {
                const name = document.getElementById("playerName").value || "Player";
                const res = await fetch("/submit-score", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ player: name, score: finalScore })
                });
                const data = await res.json();
                document.getElementById("aiBox").innerText = data.ai_comment;
                const list = document.getElementById("board");
                list.innerHTML = data.leaderboard.map(r => `<li>🏅 ${r[0]} — ${r[1]} pts</li>`).join("");
            }

            function handleAction() {
                if (gameOver) {
                    y = floorY; velocityY = 0; obstacleX = 600; score = 0; gameOver = false;
                    document.getElementById("scoreText").innerText = "Score: 0";
                } else if (y === floorY) {
                    velocityY = -15;
                }
            }

            window.addEventListener("keydown", (e) => { if (e.code === "Space") handleAction(); });
            canvas.addEventListener("click", handleAction);

            setInterval(() => {
                ctx.clearRect(0, 0, 600, 300);
                ctx.fillStyle = "#a6e3a1";
                ctx.fillRect(0, 250, 600, 50);

                if (!gameOver) {
                    y += velocityY;
                    velocityY += gravity;
                    if (y >= floorY) { y = floorY; velocityY = 0; }

                    obstacleX -= 6;
                    if (obstacleX < -30) {
                        obstacleX = 600;
                        score += 1;
                        document.getElementById("scoreText").innerText = "Score: " + score;
                    }

                    if (obstacleX > 250 && obstacleX < 320 && y > 170) {
                        gameOver = true;
                        sendScoreToBackend(score);
                    }
                }

                ctx.fillStyle = "#89b4fa";
                ctx.fillRect(280, y, 40, 40);
                ctx.fillStyle = "#f38ba8";
                ctx.fillRect(obstacleX, 210, 30, 40);

                if (gameOver) {
                    ctx.fillStyle = "white";
                    ctx.font = "bold 24px sans-serif";
                    ctx.fillText("💥 GAME OVER! Click or Space to Play Again", 55, 130);
                }
            }, 16);
        </script>
    </body>
    </html>
    """