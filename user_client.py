import httpx
from fastapi import HTTPException


def fetch_user(user_service_url: str, user_id: int) -> dict | None:
    url = f"{user_service_url}/users/{user_id}"

    try:
        response = httpx.get(url, timeout=5.0)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail="User service unavailable") from exc

    if response.status_code == 404:
        return None

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail="User service error") from exc

    return response.json()
