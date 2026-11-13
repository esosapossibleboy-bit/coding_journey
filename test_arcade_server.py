import os
from fastapi.testclient import TestClient
import arcade_server

client = TestClient(arcade_server.app)

def test_full_stack_ai_arcade(monkeypatch):
    test_db = "temp_arcade.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(arcade_server, "ARCADE_DB", test_db)

    # 1. Verify homepage serves the playable HTML5 canvas game
    home = client.get("/")
    assert home.status_code == 200
    assert "Esosa's AI Arcade Arena" in home.text

    # 2. Submit a high score (8) -> gets top-tier AI commentary + saves to SQLite
    res1 = client.post("/submit-score", json={"player": "Esosa", "score": 8})
    assert res1.status_code == 200
    assert "Legendary" in res1.json()["ai_comment"]
    assert res1.json()["leaderboard"] == [["Esosa", 8]]

    # 3. Submit a low score (2) -> gets warm-up AI commentary + sorted leaderboard
    res2 = client.post("/submit-score", json={"player": "Rival", "score": 2})
    assert "warm-up" in res2.json()["ai_comment"]
    assert res2.json()["leaderboard"] == [["Esosa", 8], ["Rival", 2]]

    if os.path.exists(test_db):
        os.remove(test_db)
