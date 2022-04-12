from calendar import month_name

import requests
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from api import schemas
from api.models import DateFact

FACT_API_URL = "http://numbersapi.com"


def get_all_dates_facts(db: Session):
    return db.query(DateFact).all()


def get_date_fact_by_id(db: Session, id: int):
    return db.query(DateFact).filter(DateFact.id == id).one_or_none()


def get_date_fact_by_date(db: Session, day: int, month: str):
    return (
        db.query(DateFact)
        .filter(DateFact.day == day, DateFact.month == month)
        .one_or_none()
    )


def get_popular_dates_facts(db: Session):
    return (
        db.query(
            func.max(DateFact.id).label("id"),
            DateFact.month,
            func.count(DateFact.month).label("days_checked"),
        )
        .group_by(DateFact.month)
        .order_by(desc("days_checked"))
        .all()
    )


def create_get_date_fact(db: Session, payload: schemas.DateFactCreate) -> DateFact:
    # fetch fact from numbersapi and store in db, then return response
    fact = requests.get(f"{FACT_API_URL}/{payload.month}/{payload.day}/date").text
    # convert month int to string repr
    payload.month = month_name[payload.month]
    date_fact = DateFact(**payload.dict(), fact=fact)
    db.add(date_fact)
    db.commit()
    db.refresh(date_fact)
    return date_fact


def delete_date_fact(db: Session, id: int) -> int:
    return db.query(DateFact).filter(DateFact.id == id).delete()
