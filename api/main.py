from calendar import month_name
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.orm import Session

from api import crud, schemas
from api.database import SessionLocal

description = """
# An API that displays fun facts provided day and month
### REDOC_URL can be found at /documentation
"""

app = FastAPI(title="Dates Fun Facts API", description=description, docs_url="/", redoc_url="/documentation")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# sanity check route
@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/dates", response_model=schemas.DateFact, status_code=201)
def create_date_fact(payload: schemas.DateFactCreate, db: Session = Depends(get_db)):
    # checks for date fact in the db
    date_fact = crud.get_date_fact_by_date(db, payload.day, month_name[payload.month])
    # if it exists, return response
    if date_fact:
        return date_fact
    return crud.create_get_date_fact(db=db, payload=payload)


@app.get("/dates", response_model=list[schemas.DateFact])
def get_all_dates_facts(db: Session = Depends(get_db)):
    dates_facts = crud.get_all_dates_facts(db)
    return dates_facts


@app.get("/dates/{id}", response_model=schemas.DateFact)
def get_single_date_fact(id: int, db: Session = Depends(get_db)):
    date_fact = crud.get_date_fact_by_id(db, id=id)
    if date_fact is None:
        raise HTTPException(status_code=404, detail="Date fact not found")
    return date_fact


@app.delete("/dates/{id}")
def delete_single_date_fact(id: int, X_API_KEY: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if X_API_KEY is None:
        raise HTTPException(status_code=400, detail="No API Key specified in header")
    if X_API_KEY != "SECRET_API_KEY":
        raise HTTPException(status_code=400, detail="Invalid API Key in header")
    
    date_fact_rows = crud.delete_date_fact(db, id)
    if date_fact_rows == 0:
        raise HTTPException(status_code=404, detail="Date fact not found")
    db.commit()
    return {"status": True, "message": "Date fact has been successfully deleted"}


@app.get("/popular", response_model=list[schemas.PopularDateFact])
def get_dates_facts_by_popularity(db: Session = Depends(get_db)):
    popular_dates_facts = crud.get_popular_dates_facts(db)
    return popular_dates_facts
