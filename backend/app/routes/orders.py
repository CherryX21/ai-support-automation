import psycopg

from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from app.database import DATABASE_URL
from app.schemas import Order, OrderUpdate


router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


# GET /orders?status=paid&min_total=150
@router.get("")
def get_orders(status: str, min_total: float):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT order_id, customer_id, status, total
                FROM orders
                WHERE status = %s
                  AND total >= %s
                ORDER BY total DESC
                """,
                (status, min_total),
            )

            return cur.fetchall()


# GET /orders/ORD-1?customer_id=CUST-001
@router.get("/{order_id}")
def get_order(order_id: str, customer_id: str | None = None):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            query = """
                SELECT
                    orders.order_id,
                    orders.customer_id,
                    customers.name AS customer_name,
                    orders.status,
                    orders.total
                FROM orders
                JOIN customers
                    ON orders.customer_id = customers.customer_id
                WHERE orders.order_id = %s
            """
            params = [order_id]

            if customer_id:
                query += " AND orders.customer_id = %s"
                params.append(customer_id)

            cur.execute(query, tuple(params))
            order = cur.fetchone()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found for this customer"
        )

    return order


# DELETE /orders/ORD-1
@router.delete("/{order_id}")
def delete_order(order_id: str):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM orders
                WHERE order_id = %s
                RETURNING order_id
                """,
                (order_id,),
            )

            result = cur.fetchone()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "order_id": result["order_id"],
        "message": "Order deleted successfully"
    }
