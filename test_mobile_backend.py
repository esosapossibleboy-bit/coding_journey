import os
from fastapi.testclient import TestClient
import mobile_backend

client = TestClient(mobile_backend.app)

def test_mobile_post_and_get_scores(monkeypatch):
    test_db = "temp_mobile_test.db"
    if os.path.exists(test_db):
        os.remove(test_db)
        
    # Point the backend to a temporary test database
    monkeypatch.setattr(mobile_backend, "DB_NAME", test_db)

    # Test 1: Mobile app sends a POST request with JSON data
    res1 = client.post("/scores", json={"player": "Esosa", "points": 500})
    assert res1.status_code == 200
    assert res1.json() == {"status": "saved", "player": "Esosa"}

    # Test 2: Mobile app sends a second score
    client.post("/scores", json={"player": "Zed", "points": 750})

    # Test 3: Mobile app fetches the sorted leaderboard via GET
    res2 = client.get("/scores")
    assert res2.status_code == 200
    assert res2.json() == {"leaderboard": [["Zed", 750], ["Esosa", 500]]}

    # Clean up temporary test database
    if os.path.exists(test_db):
        os.remove(test_db)
