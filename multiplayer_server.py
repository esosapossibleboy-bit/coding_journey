from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from multiplayer_hub import GameRoom

app = FastAPI(title="Esosa's Multiplayer 2D Arcade Hub")
room = GameRoom()
active_connections = {}

async def broadcast(message: dict):
    for ws in list(active_connections.values()):
        await ws.send_json(message)

@app.get("/", response_class=HTMLResponse)
def multiplayer_arena():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8" /><title>Multiplayer 2D Arena</title></head>
    <body style="background:#1e1e2e; color:white; font-family:sans-serif; text-align:center; padding:20px;">
        <h1>🌐 Real-Time Multiplayer 2D Arena</h1>
        <p>Open <b>two browser tabs</b> to this URL! Use <b>Arrow Keys</b> to move your square.</p>
        <input id="nameInput" value="Player1" style="padding:8px;" />
        <button onclick="connectGame()" style="padding:8px 14px;">Join Arena</button>
        <br/><br/>
        <canvas id="arena" width="500" height="350" style="background:#11111b; border:2px solid #89b4fa;"></canvas>

        <script>
            const canvas = document.getElementById("arena");
            const ctx = canvas.getContext("2d");
            let ws = null;
            let myX = 50, myY = 50;
            let players = {};

            function connectGame() {
                const name = document.getElementById("nameInput").value || "Player";
                const protocol = location.protocol === "https:" ? "wss:" : "ws:";
                ws = new WebSocket(`${protocol}//${location.host}/ws/${encodeURIComponent(name)}`);
                ws.onmessage = (event) => {
                    const msg = JSON.parse(event.data);
                    if (msg.all_players) {
                        players = msg.all_players;
                        drawArena();
                    }
                };
            }

            window.addEventListener("keydown", (e) => {
                if (!ws || ws.readyState !== WebSocket.OPEN) return;
                if (e.key === "ArrowRight") myX += 15;
                if (e.key === "ArrowLeft") myX -= 15;
                if (e.key === "ArrowUp") myY -= 15;
                if (e.key === "ArrowDown") myY += 15;
                ws.send(JSON.stringify({ x: myX, y: myY }));
            });

            function drawArena() {
                ctx.clearRect(0, 0, 500, 350);
                Object.entries(players).forEach(([name, pos], idx) => {
                    ctx.fillStyle = idx % 2 === 0 ? "#89b4fa" : "#a6e3a1";
                    ctx.fillRect(pos.x, pos.y, 35, 35);
                    ctx.fillStyle = "white";
                    ctx.font = "14px sans-serif";
                    ctx.fillText(name, pos.x, pos.y - 6);
                });
            }
        </script>
    </body>
    </html>
    """

@app.websocket("/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    await websocket.accept()
    active_connections[player_name] = websocket
    room.join_player(player_name)

    await broadcast({"event": "join", "player": player_name, "all_players": room.players})

    try:
        while True:
            data = await websocket.receive_json()
            update_msg = room.update_position(player_name, data["x"], data["y"])
            await broadcast(update_msg)
    except WebSocketDisconnect:
        del active_connections[player_name]
        room.remove_player(player_name)
        await broadcast({"event": "leave", "player": player_name, "all_players": room.players})
