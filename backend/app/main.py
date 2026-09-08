from fastapi import FastAPI

from app.routes import customers, orders, tickets


app = FastAPI()

app.include_router(orders.router)
app.include_router(customers.router)
app.include_router(tickets.router)
