import psycopg

from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from app.database import DATABASE_URL


router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)
