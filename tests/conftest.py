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


@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

        app.dependency_overrides[get_db] = override_get_db
    try:
        client = TestClient(app)
        yield client
    finally:
        pass


@pytest.fixture
def create_test_date_fact(client):
    
    date_fact = client.post("/dates", json={"day": 3, "month": 12})

    yield date_fact.json()
    
    id = date_fact.json()["id"]

    client.delete(f"/dates/{id}", headers={"X_API_KEY": "SECRET_API_KEY"})
