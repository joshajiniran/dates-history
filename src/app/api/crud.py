import requests
from sqlalchemy.orm import Session

from app.api.models import DateFact
from app.api.schemas import DateFactSchema, DateFactCreateSchema


def create_read_date_fact(db: Session, payload: DateFactCreateSchema):
    fact = requests.get(f"http://numbersapi.com/{payload.month}/{payload.day}/date")
    date_fact = DateFact(**payload.dict(), fact=fact, days_checked=1)
    db.add(date_fact)
    db.commit()
    db.refresh(date_fact)
    return date_fact


def get_date_fact_by_date(db: Session, day: int, month: int):
    date_fact = (
        db.query(DateFact)
        .filter(DateFact.day == day, DateFact.month == month)
        .one_or_none()
    )
    return date_fact


def get_date_facts(db: Session):
    return db.query(DateFact).all()


def get_popular_date_facts(db: Session):
    return db.query(DateFact).order_by(DateFact.days_checked).all()


def delete_date_fact(db: Session, id: int):
    return (
        db.query(DateFact).filter(DateFact.id == id).delete(synchronize_session=False)
    )
