# Order Service

Simple FastAPI microservice for order data with user-service integration.

## Run

From project root:

```bash
uvicorn main:app --reload --port 8002 --app-dir service-order
```

Optional environment variable (default shown):

```bash
export USER_SERVICE_URL=http://127.0.0.1:8001
```

## Database

- SQLite file: `service-order/order.db`
- Created automatically on startup
- Seed data inserted if DB is empty

## Service Linking

This service calls user service for:

- `POST /orders` : validates that `user_id` exists in user service
- `GET /orders/{order_id}/details` : returns merged order + user details

## Endpoints

- `GET /` : service health/status
- `GET /orders` : list all orders
- `GET /orders/{order_id}` : get one order by id
- `GET /orders/user/{user_id}` : list orders for a user
- `GET /orders/{order_id}/details` : order with linked user details
- `POST /orders` : create order (after user validation)

Example request body for `POST /orders`:

```json
{
  "user_id": 1,
  "item": "Phone"
}
```

## Modules

- `main.py` : API routes
- `db.py` : SQLite connection and DB initialization
- `repository.py` : order data queries
- `schemas.py` : request schema models
- `user_client.py` : HTTP client for user service calls
