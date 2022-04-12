from email.policy import default
import os

from dotenv import load_dotenv
from databases import Database
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, DateTime
from sqlalchemy.sql import func


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()

dates = Table(
    "dates",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("day", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("fact", String(255), nullable=False),
    Column("days_checked", Integer),
    Column("created", DateTime, default=func.now(), nullable=False),
)

database = Database(DATABASE_URL)