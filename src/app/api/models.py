from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db import Base


class DateFact(Base):

    __tablename__ = "dates_facts"

    id = (Column(Integer, primary_key=True, autoincrement=True),)
    day = (Column(Integer, nullable=False),)
    month = (Column(Integer, nullable=False),)
    fact = (Column(String(255), nullable=False),)
    days_checked = (Column(Integer),)
    created = Column(DateTime, default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"DateFact<{self.day}/{self.month}>"
