import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "order.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item TEXT NOT NULL
            )
            """
        )

        existing_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        if existing_count == 0:
            conn.executemany(
                "INSERT INTO orders(user_id, item) VALUES (?, ?)",
                [(1, "Book"), (2, "Laptop")],
            )
        conn.commit()
