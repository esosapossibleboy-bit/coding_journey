import os
from fastapi.testclient import TestClient
import habit_server

client = TestClient(habit_server.app)

def test_mobile_habit_api_flow(monkeypatch):
    test_db = "temp_habits.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(habit_server, "HABIT_DB", test_db)

    # 1. Start with empty habit list
    res0 = client.get("/habits")
    assert res0.status_code == 200
    assert res0.json() == {"habits": []}

    # 2. Create a new habit
    res1 = client.post("/habits", json={"name": "Read 10 pages"})
    assert res1.status_code == 200
    assert res1.json()["habits"][0]["name"] == "Read 10 pages"
    assert res1.json()["habits"][0]["streak"] == 0

    # 3. Complete the habit for two consecutive days -> streak reaches 2!
    c1 = client.post("/habits/1/complete?today=2026-11-12")
    assert c1.status_code == 200
    assert c1.json()["streak"] == 1

    c2 = client.post("/habits/1/complete?today=2026-11-13")
    assert c2.status_code == 200
    assert c2.json()["streak"] == 2

    # 4. Completing a non-existent habit returns 404
    c_missing = client.post("/habits/99/complete")
    assert c_missing.status_code == 404

    if os.path.exists(test_db):
        os.remove(test_db)
