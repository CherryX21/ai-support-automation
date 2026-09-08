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


# GET /orders/ORD-1
@router.get("/{order_id}")
def get_order(order_id: str):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
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
                """,
                (order_id,),
            )

            order = cur.fetchone()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# POST /orders
@router.post("")
def create_order(order: Order):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO orders (
                    order_id,
                    customer_id,
                    status,
                    total
                )
                VALUES (%s, %s, %s, %s)
                RETURNING order_id, customer_id, status, total
                """,
                (
                    order.order_id,
                    order.customer_id,
                    order.status,
                    order.total,
                ),
            )

            return cur.fetchone()


# PATCH /orders/ORD-1
@router.patch("/{order_id}")
def update_order(order_id: str, order_update: OrderUpdate):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE orders
                SET status = %s
                WHERE order_id = %s
                RETURNING order_id, customer_id, status, total
                """,
                (
                    order_update.status,
                    order_id,
                ),
            )

            result = cur.fetchone()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return result


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
