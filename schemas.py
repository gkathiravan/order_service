from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    item: str
