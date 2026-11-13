import os
from fastapi.testclient import TestClient
import study_server
from rate_limiter import RateLimiter

client = TestClient(study_server.app)

def test_study_buddy_backend_flow(monkeypatch):
    test_db = "temp_study_buddy.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(study_server, "STUDY_DB", test_db)
    monkeypatch.setattr(study_server, "ai_limiter", RateLimiter(max_requests=2))

    # 1. Register & Login
    reg = client.post("/register", json={"username": "esosa", "password": "secret"})
    assert reg.status_code == 200
    uid = reg.json()["user_id"]

    bad_login = client.post("/login", json={"username": "esosa", "password": "wrong"})
    assert bad_login.status_code == 401

    good_login = client.post("/login", json={"username": "esosa", "password": "secret"})
    assert good_login.status_code == 200
    assert good_login.json()["user_id"] == uid

    # 2. Save a study note & receive auto-generated flashcards
    note_res = client.post("/notes", json={
        "user_id": uid,
        "title": "Caching",
        "content": "Caching stores answers in memory for fast lookup."
    })
    assert note_res.status_code == 200
    assert len(note_res.json()["flashcards"]) == 1

    # 3. Ask AI Tutor (allowed twice, blocked on 3rd request by RateLimiter!)
    ask1 = client.post("/tutor/ask", json={"user_id": uid, "question": "What does caching do?"})
    assert ask1.status_code == 200
    assert "Caching stores answers" in ask1.json()["answer"]

    ask2 = client.post("/tutor/ask", json={"user_id": uid, "question": "Explain caching again"})
    assert ask2.status_code == 200

    ask3 = client.post("/tutor/ask", json={"user_id": uid, "question": "Spam question"})
    assert ask3.status_code == 429

    if os.path.exists(test_db):
        os.remove(test_db)
