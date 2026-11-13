import sqlite3

def init_finance_db(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            amount REAL,
            kind TEXT,
            category TEXT
        )
    """)
    conn.commit()


def add_transaction(conn, title, amount, kind, category):
    cursor = conn.cursor()

    # Insert the transaction
    cursor.execute("""
        INSERT INTO transactions (title, amount, kind, category)
        VALUES (?, ?, ?, ?)
    """, (title, amount, kind, category))

    # Commit changes
    conn.commit()

    # Return the ID of the inserted transaction
    return cursor.lastrowid


def get_financial_summary(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT amount, kind, category FROM transactions")
    rows = cursor.fetchall()

    total_income = 0.0
    total_expenses = 0.0
    by_category = {}

    # Calculate income, expenses, and category totals
    for amount, kind, category in rows:
        if kind == "income":
            total_income += amount

        elif kind == "expense":
            total_expenses += amount
            by_category[category] = by_category.get(category, 0.0) + amount

    # Return financial summary
    return {
        "income": total_income,
        "expenses": total_expenses,
        "balance": total_income - total_expenses,
        "by_category": by_category
    }