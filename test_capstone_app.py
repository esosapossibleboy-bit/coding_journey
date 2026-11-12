import os
from fastapi.testclient import TestClient
import capstone_app

client = TestClient(capstone_app.app)

def test_full_capstone_integration(monkeypatch):
    test_db = "temp_capstone.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(capstone_app, "CAPSTONE_DB", test_db)

    # 1. Test AI Mood + Chatbot working together
    ai_res = client.get("/ai/chat?message=I love this, what is the price?")
    assert ai_res.status_code == 200
    assert ai_res.json() == {
        "mood": "Positive",
        "reply": "Our basic plan is free, and Pro is $10 per month."
    }

    # 2. Test 2D Game Engine over HTTP API
    move_res = client.post("/game/move", json={"x": 2, "y": 2, "direction": "UP", "map_size": 5})
    assert move_res.status_code == 200
    assert move_res.json() == {"x": 2, "y": 3}

    # 3. Test SQL Leaderboard persistence
    score_res = client.post("/game/score?player=Esosa&points=1000")
    assert score_res.status_code == 200
    assert score_res.json() == {"leaderboard": [["Esosa", 1000]]}

    if os.path.exists(test_db):
        os.remove(test_db)
