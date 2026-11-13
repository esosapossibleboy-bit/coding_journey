import sqlite3
from finance_db import init_finance_db, add_transaction, get_financial_summary

def test_personal_finance_engine():
    conn = sqlite3.connect(":memory:")
    init_finance_db(conn)

    # 1. Record income and expenses across categories
    add_transaction(conn, "Paycheck", 1000.0, "income", "Salary")
    add_transaction(conn, "Groceries", 120.0, "expense", "Food")
    add_transaction(conn, "Pizza", 30.0, "expense", "Food")
    add_transaction(conn, "Indie Game", 50.0, "expense", "Entertainment")

    # 2. Verify totals, remaining balance, and category grouping
    summary = get_financial_summary(conn)
    assert summary["income"] == 1000.0
    assert summary["expenses"] == 200.0
    assert summary["balance"] == 800.0
    assert summary["by_category"] == {"Food": 150.0, "Entertainment": 50.0}
    conn.close()
