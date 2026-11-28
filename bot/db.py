from datetime import date
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
    
def add_meal(user_id: int, meal: dict):
    """Зберігає прийом їжі. meal має поля dish, weight_g, calories, protein, fat, carbs."""
    with _connect() as conn:
        conn.execute(
            "INSERT INTO meals (user_id, dish, weight_g, calories, protein, fat, carbs, eaten_on) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                meal["dish"],
                meal.get("weight_g"),
                meal["calories"],
                meal["protein"],
                meal["fat"],
                meal["carbs"],
                date.today().isoformat(),
            ),
        )