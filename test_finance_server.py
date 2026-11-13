import os
from fastapi.testclient import TestClient
import finance_server

client = TestClient(finance_server.app)

def test_ai_finance_app_flow(monkeypatch):
    test_db = "temp_finance.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    monkeypatch.setattr(finance_server, "FINANCE_DB", test_db)

    # 1. Dashboard loads cleanly
    home = client.get("/")
    assert home.status_code == 200
    assert "AI Personal Finance & Budget App" in home.text

    # 2. Add $1,000 income + $150 Food expense -> saving 85% -> "Great job saving!"
    client.post("/transactions", json={"title": "Paycheck", "amount": 1000, "kind": "income", "category": "Salary"})
    res = client.post("/transactions", json={"title": "Groceries", "amount": 150, "kind": "expense", "category": "Food"})
    assert res.status_code == 200
    assert res.json()["summary"]["balance"] == 850.0
    assert "Great job saving" in res.json()["advice"]
    assert "Food" in res.json()["advice"]

    # 3. Overspend $950 on Games -> triggers overspending warning!
    res2 = client.post("/transactions", json={"title": "New Console", "amount": 950, "kind": "expense", "category": "Games"})
    assert "Overspending" in res2.json()["advice"]
    assert "Games" in res2.json()["advice"]

    if os.path.exists(test_db):
        os.remove(test_db)
