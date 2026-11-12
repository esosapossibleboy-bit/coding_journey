import sqlite3
from leaderboard_db import setup_database, save_score, get_all_scores

def test_sql_leaderboard():
    # Create an in-memory SQLite database just for testing
    conn = sqlite3.connect(":memory:")
    setup_database(conn)

    # Save three player scores
    save_score(conn, "Esosa", 150)
    save_score(conn, "Aria", 300)
    save_score(conn, "Leo", 90)

    # Fetch scores sorted from highest to lowest
    results = get_all_scores(conn)
    assert results == [("Aria", 300), ("Esosa", 150), ("Leo", 90)]
    conn.close()
