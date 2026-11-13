import os
from fastapi.testclient import TestClient
import finance_server
from rate_limiter import RateLimiter

client = TestClient(finance_server.app)

def test_private_multiuser_finance_security(monkeypatch):
    test_db = "temp_finance_secure.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(finance_server, "FINANCE_DB", test_db)
    monkeypatch.setattr(finance_server, "ADMIN_KEY", "secret-admin-key")
    monkeypatch.setattr(finance_server, "auth_limiter", RateLimiter(max_requests=20))
    monkeypatch.setattr(finance_server, "tx_limiter", RateLimiter(max_requests=20))

    # 1. Unauthenticated access is blocked with 401
    assert client.get("/summary").status_code == 401

    # 2. Weak passwords without uppercase/numbers/symbols are rejected with 422
    weak = client.post("/auth/register", json={"email": "weak@test.com", "name": "Weak", "password": "password123"})
    assert weak.status_code == 422

    # 3. Register two separate users with strong passwords
    esosa = client.post("/auth/register", json={"email": "esosa@test.com", "name": "Esosa", "password": "Password123!"}).json()
    hacker = client.post("/auth/register", json={"email": "hacker@test.com", "name": "Hacker", "password": "Password123!"}).json()

    esosa_headers = {"Authorization": f"Bearer {esosa['token']}"}
    hacker_headers = {"Authorization": f"Bearer {hacker['token']}"}

    # 4. Esosa creates income & expense
    client.post("/transactions", headers=esosa_headers, json={"title": "Paycheck", "amount": 1000, "kind": "income", "category": "Job"})
    tx_res = client.post("/transactions", headers=esosa_headers, json={"title": "Lunch", "amount": 20, "kind": "expense", "category": "Food"})
    tx_id = tx_res.json()["summary"]["transactions"][0]["id"]

    # 5. Hacker CANNOT see, edit, or delete Esosa's private budget!
    assert client.get("/summary", headers=hacker_headers).json()["summary"]["balance"] == 0.0
    assert client.put(f"/transactions/{tx_id}", headers=hacker_headers, json={"title": "Stolen", "amount": 999, "kind": "expense", "category": "Food"}).status_code == 404
    assert client.delete(f"/transactions/{tx_id}", headers=hacker_headers).status_code == 404

    # 6. Esosa edits and deletes his own entry cleanly
    edit_res = client.put(f"/transactions/{tx_id}", headers=esosa_headers, json={"title": "Healthy Lunch", "amount": 12, "kind": "expense", "category": "Food"})
    assert edit_res.status_code == 200
    assert edit_res.json()["summary"]["balance"] == 988.0

    del_res = client.delete(f"/transactions/{tx_id}", headers=esosa_headers)
    assert del_res.status_code == 200
    assert del_res.json()["summary"]["balance"] == 1000.0

    # 7. Admin user counter shows 2 users without exposing password hashes
    assert client.get("/admin/users?key=wrong").status_code == 403
    stats = client.get("/admin/users?key=secret-admin-key").json()
    assert stats["total_users"] == 2
    assert "password_hash" not in str(stats)

    if os.path.exists(test_db):
        os.remove(test_db)
