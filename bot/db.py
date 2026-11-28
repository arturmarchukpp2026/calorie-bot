import sqlite3

DB_PATH = "calories.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Створює таблицю meals, якщо її ще немає."""
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                dish TEXT NOT NULL,
                weight_g REAL,
                calories REAL,
                protein REAL,
                fat REAL,
                carbs REAL,
                eaten_on TEXT NOT NULL
            )
        """)