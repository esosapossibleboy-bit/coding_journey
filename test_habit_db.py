import sqlite3
from habit_db import init_habit_db, create_habit, complete_habit

def test_habit_streak_engine():
    conn = sqlite3.connect(":memory:")
    init_habit_db(conn)

    hid = create_habit(conn, "Code for 30 minutes")
    assert hid == 1

    # Day 1: First completion starts streak at 1
    assert complete_habit(conn, hid, "2026-11-10") == 1

    # Completing again on the SAME day keeps streak at 1 (no double counting!)
    assert complete_habit(conn, hid, "2026-11-10") == 1

    # Day 2 (consecutive day): Streak increases to 2!
    assert complete_habit(conn, hid, "2026-11-11") == 2

    # Skipped Nov 12, completed on Nov 13 -> Streak resets to 1!
    assert complete_habit(conn, hid, "2026-11-13") == 1
    conn.close()
