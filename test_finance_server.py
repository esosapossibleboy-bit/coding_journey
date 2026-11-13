import os
from fastapi.testclient import TestClient
import finance_server
from rate_limiter import RateLimiter

client = TestClient(finance_server.app)

def test_ai_finance_app_flow(monkeypatch):
    test_db = "temp_finance.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(finance_server, "FINANCE_DB", test_db)
    monkeypatch.setattr(finance_server, "tx_limiter", RateLimiter(max_requests=10))

    # 1. Dashboard loads with security headers and mobile viewport tag
    home = client.get("/")
    assert home.status_code == 200
    assert home.headers["X-Frame-Options"] == "DENY"
    assert 'name="viewport"' in home.text

    # 2. Reject negative dollar amounts and invalid transaction types
    bad_amount = client.post("/transactions", json={"title": "Hack", "amount": -50, "kind": "expense", "category": "Food"})
    assert bad_amount.status_code == 422

    bad_kind = client.post("/transactions", json={"title": "Hack", "amount": 50, "kind": "steal", "category": "Food"})
    assert bad_kind.status_code == 422

    # 3. Valid income & expense flow works seamlessly
    client.post("/transactions", json={"title": "Paycheck", "amount": 1000, "kind": "income", "category": "Salary"})
    res = client.post("/transactions", json={"title": "Groceries", "amount": 150, "kind": "expense", "category": "Food"})
    assert res.status_code == 200
    assert res.json()["summary"]["balance"] == 850.0
    assert "Great job saving" in res.json()["advice"]

    if os.path.exists(test_db):
        os.remove(test_db)
