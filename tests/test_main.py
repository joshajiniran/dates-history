def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_get_all_dates_facts(client):
    response = client.get("/dates")
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_get_single_date_fact(client, create_test_date_fact):
    date_fact = create_test_date_fact
    response = client.get(f"/dates/{date_fact['id']}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "day" in response.json()
    assert isinstance(response.json()["month"], str)


def test_get_non_existing_single_date_fact(client):
    response = client.get("/dates/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Date fact not found"}


def test_get_single_date_fact_with_invalid_id(client):
    response = client.get("/dates/id")
    assert response.status_code == 422


def test_create_date_fact(client):
    response = client.post("/dates", json={"day": 3, "month": 11})
    assert response.status_code == 201
    assert "fact" in response.json()
    assert response.json()["month"] == "November"


def test_create_date_fact_with_invalid_body(client):
    response = client.post("/dates", json={"day": "3", "month": "march"})
    assert response.status_code == 422
    

def test_create_date_fact_with_month_day_excess(client):
    # this ought to raise February does not contain 31 days error
    # this also applies to calling {"day": 31, ...} on months with 30 days
    # numbersapi.com returns a result that protrudes into the next month e.g
    # {"day": 31, "month": 2} gives a 2nd of March date fact which is incosistent
    response = client.post("/dates", json={"day": 31, "month": 2})
    assert response.status_code == 400
    assert "detail" in response.json()


def test_get_dates_facts_rank_by_days_checked(client):
    response = client.get("/popular")
    assert response.status_code == 200
    assert len(response.json()) >= 0
    assert "days_checked" in response.json()[0] if len(response.json()) > 0 else None


def test_delete_date_fact_by_id(client, create_test_date_fact):
    date_fact = create_test_date_fact
    response = client.delete(f"/dates/{date_fact['id']}", headers={"X-API-KEY": "SECRET_API_KEY"})
    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "message": "Date fact has been successfully deleted",
    }


def test_delete_non_existing_date_fact(client):
    response = client.delete("/dates/9999", headers={"X-API-KEY": "SECRET_API_KEY"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Date fact not found"}


def test_delete_date_fact_by_id_no_api_key(client):
    response = client.delete("/dates/1")
    assert response.status_code == 400
    assert response.json() == {"detail": "No API Key specified in header"}


def test_delete_date_fact_by_id_invalid_api_key(client):
    response = client.delete("/dates/1", headers={"X-API-KEY": "SECRET_KEY"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid API Key in header"}
