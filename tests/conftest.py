from functools import lru_cache

import pytest
from api.config import Settings
from api.database import Base
from api.main import app, get_db
from api.models import DateFact
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.test_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_app():
    try:
        client = TestClient(app)
        yield client
    finally:
        pass


@pytest.fixture(scope="function")
def create_test_date_fact(test_app):
    db = next(override_get_db())
    date_fact = DateFact(
        id=1,
        day=1,
        month="January",
        fact="On 1st January 1890, King Edwards became a Junior Developer",
    )
    db.add(date_fact)
    db.commit()

    yield

    db.query(DateFact).filter(DateFact.id == 1).delete()
    db.commit()
