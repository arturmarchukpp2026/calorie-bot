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


def delete_last_meal(user_id: int):
    """Видаляє останній запис користувача. Повертає видалений запис або None."""
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, dish, calories FROM meals WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        if row is None:
            return None
        conn.execute("DELETE FROM meals WHERE id = ?", (row[0],))
    return {"dish": row[1], "calories": row[2] or 0}
    
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
