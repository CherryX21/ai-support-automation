from pydantic import BaseModel


class Order(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total: float


class OrderUpdate(BaseModel):
    status: str
