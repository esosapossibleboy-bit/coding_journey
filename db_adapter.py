import os
import sqlite3

def get_db_connection(sqlite_path: str = "finance.db"):
    db_url = os.getenv("DATABASE_URL", "")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    if db_url:
        import psycopg2
        return PostgresConnectionWrapper(psycopg2.connect(db_url))
    return sqlite3.connect(sqlite_path)

class PostgresCursorWrapper:
    def __init__(self, cursor):
        self._cursor = cursor
        self.lastrowid = None
        self.rowcount = 0

    def execute(self, sql: str, params=()):
        # Translate SQLite syntax to PostgreSQL syntax automatically
        pg_sql = (
            sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
            .replace("?", "%s")
        )
        is_insert = pg_sql.strip().upper().startswith("INSERT INTO")
        if is_insert and "RETURNING" not in pg_sql.upper():
            pg_sql = pg_sql.rstrip().rstrip(";") + " RETURNING id"

        self._cursor.execute(pg_sql, params)
        self.rowcount = self._cursor.rowcount
        if is_insert:
            row = self._cursor.fetchone()
            self.lastrowid = row if row else None

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

class PostgresConnectionWrapper:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return PostgresCursorWrapper(self._conn.cursor())

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()
