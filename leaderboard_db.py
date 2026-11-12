import sqlite3


def setup_database(connection):
    # Creates the scores table if it does not exist yet
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS scores (player TEXT, points INTEGER)"
    )
    connection.commit()


def save_score(connection, player, points):
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO scores (player, points) VALUES (?, ?)", (player, points)
    )
    connection.commit()


def get_all_scores(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT player, points FROM scores ORDER BY points DESC")
    return cursor.fetchall()
