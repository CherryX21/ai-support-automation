from pydantic import BaseModel


class Order(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total: float


class OrderUpdate(BaseModel):
    status: str


class TicketCreate(BaseModel):
    customer_id: str
    order_id: str | None = None
    category: str
    message: str
