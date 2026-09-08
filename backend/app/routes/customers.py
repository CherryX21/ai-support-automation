import psycopg

from fastapi import APIRouter
from psycopg.rows import dict_row

from app.database import DATABASE_URL


router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

# GET /customers/CUST-001/orders
@router.get("/{customer_id}/orders")
def get_customer_orders(customer_id: str):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT order_id, status, total, created_at
                FROM orders
                WHERE customer_id = %s
                ORDER BY created_at DESC, order_id DESC
                """,
                (customer_id,),
            )

            return cur.fetchall()
