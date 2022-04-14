from typing import Optional
from pydantic import BaseModel, Field


class DateFactBase(BaseModel):
    day: int = Field(gt=0, le=31, description="Day of the month. Must be from 1 to 31")
    month: str


class DateFactCreate(DateFactBase):
    month: int = Field(gt=0, le=12, description="Month of a year. Must be from 1 to 12")


class DateFact(DateFactBase):
    id: int
    fact: str

    class Config:
        orm_mode = True


class PopularDateFact(BaseModel):
    id: int
    month: str
    days_checked: int

    class Config:
        orm_mode = True
