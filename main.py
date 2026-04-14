import os

from fastapi import FastAPI, HTTPException

from db import init_db
from repository import create_new_order, get_order_by_id, list_all_orders, list_orders_for_user
from schemas import OrderCreate
from user_client import fetch_user

app = FastAPI(title="Order Service", version="1.0.0")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://127.0.0.1:8001")


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root() -> dict:
    return {"service": "order-service", "status": "ok"}


@app.get("/orders/{order_id}")
def get_order(order_id: int) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/orders")
def list_orders() -> dict:
    return {"orders": list_all_orders()}


@app.get("/orders/user/{user_id}")
def list_orders_by_user(user_id: int) -> dict:
    matched_orders = list_orders_for_user(user_id)
    return {"orders": matched_orders, "count": len(matched_orders)}


@app.post("/orders")
def create_order(payload: OrderCreate) -> dict:
    user = fetch_user(USER_SERVICE_URL, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in user-service")

    return create_new_order(payload.user_id, payload.item)


@app.get("/orders/{order_id}/details")
def get_order_details(order_id: int) -> dict:
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    user = fetch_user(USER_SERVICE_URL, order["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="Linked user not found in user-service")

    return {"order": order, "user": user}
