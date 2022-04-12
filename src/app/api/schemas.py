# Pydantic model
from pydantic import BaseModel, Field


class DateFactCreateSchema(BaseModel):
    day: int = Field(..., gt=1, le=31, description="The day must be from 1 to 31")
    month: int = Field(..., gt=1, le=12, description="Month must be from 1 to 12")


class DateFactSchema(DateFactCreateSchema):
    month: str
    fact: str


class PopularDateFactSchema(DateFactSchema):
    days_checked: int


class DateFactDB(PopularDateFactSchema):
    id: int

    class Config:
        orm_mode = True
