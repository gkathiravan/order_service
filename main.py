import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Order Service", version="1.0.0")

DB_PATH = Path(__file__).resolve().parent / "order.db"


class OrderCreate(BaseModel):
    user_id: int
    item: str


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
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


@app.get("/")
def root() -> dict:
    return {"service": "order-service", "status": "ok"}


@app.get("/orders/{order_id}")
def get_order(order_id: int) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, user_id, item FROM orders WHERE id = ?",
            (order_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"id": row["id"], "user_id": row["user_id"], "item": row["item"]}


@app.get("/orders")
def list_orders() -> dict:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, user_id, item FROM orders ORDER BY id").fetchall()

    orders = [{"id": row["id"], "user_id": row["user_id"], "item": row["item"]} for row in rows]
    return {"orders": orders}


@app.get("/orders/user/{user_id}")
def list_orders_by_user(user_id: int) -> dict:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, user_id, item FROM orders WHERE user_id = ? ORDER BY id",
            (user_id,),
        ).fetchall()

    matched_orders = [{"id": row["id"], "user_id": row["user_id"], "item": row["item"]} for row in rows]
    return {"orders": matched_orders, "count": len(matched_orders)}


@app.post("/orders")
def create_order(payload: OrderCreate) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO orders(user_id, item) VALUES (?, ?)",
            (payload.user_id, payload.item),
        )
        conn.commit()

    return {"id": cursor.lastrowid, "user_id": payload.user_id, "item": payload.item}
