import sqlite3
from study_db import (
    hash_password,
    init_study_db,
    register_user,
    verify_user,
    add_study_note,
    get_user_notes,
)

def test_study_buddy_users_and_notes():
    conn = sqlite3.connect(":memory:")
    init_study_db(conn)

    # 1. Password hashing never stores plain text
    assert hash_password("mysecret") != "mysecret"

    # 2. Register two users & verify login
    esosa_id = register_user(conn, "esosa", "pass123")
    aria_id = register_user(conn, "aria", "pass456")
    assert esosa_id == 1
    assert aria_id == 2

    # Duplicate username should be rejected cleanly
    assert register_user(conn, "esosa", "otherpass") is None

    # Correct password returns user_id; wrong password returns None
    assert verify_user(conn, "esosa", "pass123") == 1
    assert verify_user(conn, "esosa", "wrongpass") is None

    # 3. Each user's study notes stay private to their user_id!
    add_study_note(conn, esosa_id, "Python", "Lists use square brackets.")
    add_study_note(conn, aria_id, "React", "useState stores component memory.")

    assert get_user_notes(conn, esosa_id) == [("Python", "Lists use square brackets.")]
    assert get_user_notes(conn, aria_id) == [("React", "useState stores component memory.")]
    conn.close()
