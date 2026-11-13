import sqlite3
import hashlib
import hmac
import secrets

def hash_password_salted(password: str, salt: str = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${dk.hex()}"

def verify_password_salted(password: str, stored_value: str) -> bool:
    if not stored_value or "$" not in stored_value:
        return False
    salt, _ = stored_value.split("$", 1)
    expected = hash_password_salted(password, salt)
    return hmac.compare_digest(expected, stored_value)

def init_finance_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finance_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            name TEXT,
            password_hash TEXT,
            google_sub TEXT UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            amount REAL,
            kind TEXT,
            category TEXT
        )
    """)
    conn.commit()

def register_email_user(conn, email, name, password):
    cursor = conn.cursor()
    secure_hash = hash_password_salted(password)
    try:
        cursor.execute(
            "INSERT INTO finance_users (email, name, password_hash) VALUES (?, ?, ?)",
            (email.lower().strip(), name.strip(), secure_hash),
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None

def verify_email_user(conn, email, password):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, password_hash FROM finance_users WHERE email = ?",
        (email.lower().strip(),),
    )
    row = cursor.fetchone()
    if row and verify_password_salted(password, row[2]):
        return row[0], row[1]
    return None

def register_or_login_google(conn, email, name, google_sub):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name FROM finance_users WHERE google_sub = ? OR email = ?",
        (google_sub, email.lower().strip()),
    )
    row = cursor.fetchone()
    if row:
        return row[0], row[1]
    cursor.execute(
        "INSERT INTO finance_users (email, name, google_sub) VALUES (?, ?, ?)",
        (email.lower().strip(), name.strip(), google_sub),
    )
    conn.commit()
    return cursor.lastrowid, name.strip()

def get_user_stats(conn):
    # Safe admin overview: counts users and lists public metadata WITHOUT password hashes!
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, google_sub, created_at FROM finance_users ORDER BY id ASC")
    users = [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "auth_type": "Google" if r[3] else "Email",
            "joined": r[4],
        }
        for r in cursor.fetchall()
    ]
    return {"total_users": len(users), "users": users}

def add_transaction(conn, user_id, title, amount, kind, category):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (user_id, title, amount, kind, category) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, amount, kind, category),
    )
    conn.commit()
    return cursor.lastrowid

def update_transaction(conn, user_id, tx_id, title, amount, kind, category):
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE transactions
        SET title = ?, amount = ?, kind = ?, category = ?
        WHERE id = ? AND user_id = ?
        """,
        (title, amount, kind, category, tx_id, user_id),
    )
    conn.commit()
    return cursor.rowcount > 0

def delete_transaction(conn, user_id, tx_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (tx_id, user_id))
    conn.commit()
    return cursor.rowcount > 0

def get_user_transactions(conn, user_id):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, amount, kind, category FROM transactions WHERE user_id = ? ORDER BY id DESC",
        (user_id,),
    )
    return [
        {"id": r[0], "title": r[1], "amount": r[2], "kind": r[3], "category": r[4]}
        for r in cursor.fetchall()
    ]

def get_financial_summary(conn, user_id):
    items = get_user_transactions(conn, user_id)
    total_income = sum(tx["amount"] for tx in items if tx["kind"] == "income")
    total_expenses = sum(tx["amount"] for tx in items if tx["kind"] == "expense")
    by_category = {}
    for tx in items:
        if tx["kind"] == "expense":
            by_category[tx["category"]] = by_category.get(tx["category"], 0.0) + tx["amount"]

    return {
        "income": total_income,
        "expenses": total_expenses,
        "balance": total_income - total_expenses,
        "by_category": by_category,
        "transactions": items,
    }
