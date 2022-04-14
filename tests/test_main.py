from .conftest import test_app


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
    

def test_get_all_dates_facts(test_app):
    response = test_app.get("/dates")
    assert response.status_code == 200
    assert len(response.json()) >= 0
    

def test_get_single_date_fact(test_app):
    response = test_app.get("/dates/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "day" in response.json()
    assert isinstance(response.json()["month"], str)
    
def test_get_non_existing_single_date_fact(test_app):
    response = test_app.get("/dates/999")
    assert response.status_code == 404
    assert response.json() == { "detail": "Date fact not found"}
    
def test_get_single_date_fact_with_invalid_id(test_app):
    response = test_app.get("/dates/id")
    assert response.status_code == 422
    

def test_create_date_fact(test_app):
    response = test_app.post(
        "/dates",
        json={
            "day": 3,
            "month": 11
        }
    )
    assert response.status_code == 201
    assert "fact" in response.json()
    assert response.json()["month"] == "November"

def test_create_date_fact_with_invalid_body(test_app):
    response = test_app.post(
        "/dates",
        json={
            "day": '3',
            "month": "march"
        }
    )
    assert response.status_code == 422

def test_get_dates_facts_rank_by_days_checked(test_app):
    response = test_app.get("/popular")
    assert response.status_code == 200
    assert len(response.json()) >= 0
    assert "days_checked" in response.json()[0] if len(response.json()) > 0 else None
    

def test_delete_date_fact_by_id(test_app):
    response = test_app.get(
        "/dates/1",
        headers={
            "X-API-KEY": "SECRET_API_KEY"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": True, "message": "Date fact has been successfully deleted"}
    
def test_delete_non_existing_date_fact(test_app):
    response = test_app.get(
        "/dates/9999",
        headers={
            "X-API-KEY": "SECRET_API_KEY"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Date fact not found"}
    

def test_delete_date_fact_by_id_no_api_key(test_app):
    response = test_app.get(
        "/dates/1"
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "No API Key specified in header"}
    

def test_delete_date_fact_by_id_invalid_api_key(test_app):
    response = test_app.get(
        "/dates/1",
        headers={
            "X-API-KEY": "SECRET_KEY"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid API Key in header"}
