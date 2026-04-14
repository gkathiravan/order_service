from db import get_connection


def _row_to_order(row) -> dict:
    return {"id": row["id"], "user_id": row["user_id"], "item": row["item"]}


def get_order_by_id(order_id: int) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, user_id, item FROM orders WHERE id = ?",
            (order_id,),
        ).fetchone()

    if not row:
        return None
    return _row_to_order(row)


def list_all_orders() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, user_id, item FROM orders ORDER BY id").fetchall()

    return [_row_to_order(row) for row in rows]


def list_orders_for_user(user_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, user_id, item FROM orders WHERE user_id = ? ORDER BY id",
            (user_id,),
        ).fetchall()

    return [_row_to_order(row) for row in rows]


def create_new_order(user_id: int, item: str) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO orders(user_id, item) VALUES (?, ?)",
            (user_id, item),
        )
        conn.commit()

    return {"id": cursor.lastrowid, "user_id": user_id, "item": item}
