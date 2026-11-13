import sqlite3
from finance_db import (
    hash_password_salted,
    verify_password_salted,
    init_finance_db,
    register_email_user,
    verify_email_user,
    register_or_login_google,
    get_user_stats,
    add_transaction,
    update_transaction,
    delete_transaction,
    get_financial_summary,
)

def test_salted_auth_user_stats_and_private_crud():
    conn = sqlite3.connect(":memory:")
    init_finance_db(conn)

    # 1. Salted password hashing check
    h1 = hash_password_salted("MySecret123")
    h2 = hash_password_salted("MySecret123")
    assert h1 != h2
    assert verify_password_salted("MySecret123", h1) is True
    assert verify_password_salted("WrongPass", h1) is False

    # 2. Register two users with custom currencies & unpack (id, name, currency)
    esosa_id = register_email_user(conn, "esosa@example.com", "Esosa", "MySecret123", "€")
    aria_id, _, aria_cur = register_or_login_google(conn, "aria@gmail.com", "Aria", "google-sub-999", "₦")
    assert aria_cur == "₦"
    assert verify_email_user(conn, "esosa@example.com", "MySecret123") == (esosa_id, "Esosa", "€")

    stats = get_user_stats(conn)
    assert stats["total_users"] == 2
    assert "password_hash" not in str(stats)

    # 3. Private budget CRUD & local continent timestamp check
    add_transaction(conn, esosa_id, "Salary", 2000.0, "income", "Work", "2026-11", "13 Nov 2026, 21:35 (Europe/Berlin)")
    tx_id = add_transaction(conn, esosa_id, "Burger", 25.0, "expense", "Food", "2026-11")

    assert update_transaction(conn, aria_id, tx_id, "Hack", 9999.0, "expense", "Food", "2026-11") is False
    assert delete_transaction(conn, aria_id, tx_id) is False
    assert update_transaction(conn, esosa_id, tx_id, "Salad", 15.0, "expense", "Food", "2026-11") is True
    assert get_financial_summary(conn, esosa_id, "2026-11")["balance"] == 1985.0
    assert delete_transaction(conn, esosa_id, tx_id) is True
    assert get_financial_summary(conn, esosa_id, "2026-11")["balance"] == 2000.0
    conn.close()
