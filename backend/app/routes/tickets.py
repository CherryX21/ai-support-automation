import psycopg

from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from app.database import DATABASE_URL
from app.schemas import TicketCreate


router = APIRouter(
	prefix="/tickets",
	tags=["tickets"],
)


# POST /tickets
@router.post("", status_code=201)
def create_ticket(ticket: TicketCreate):
	with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
		with conn.cursor() as cur:
			cur.execute(
				"""
				SELECT 1
				FROM customers
				WHERE customer_id = %s
				""",
				(ticket.customer_id,),
			)

			if cur.fetchone() is None:
				raise HTTPException(
					status_code=404,
					detail="Customer not found",
				)

			if ticket.order_id is not None:
				cur.execute(
					"""
					SELECT 1
					FROM orders
					WHERE order_id = %s
					  AND customer_id = %s
					""",
					(ticket.order_id, ticket.customer_id),
				)

				if cur.fetchone() is None:
					raise HTTPException(
						status_code=404,
						detail="Order not found for this customer",
					)

			cur.execute(
				"""
				INSERT INTO support_tickets (
					customer_id,
					order_id,
					category,
					message
				)
				VALUES (%s, %s, %s, %s)
				RETURNING
					ticket_id,
					customer_id,
					order_id,
					category,
					status,
					message,
					created_at,
					updated_at
				""",
				(
					ticket.customer_id,
					ticket.order_id,
					ticket.category,
					ticket.message,
				),
			)

			return cur.fetchone()
