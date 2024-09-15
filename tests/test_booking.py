from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_booking(test_client: TestClient, db_session: Session, test_booking_data, auth_headers):
    response = test_client.post("/api/v1/bookings/", json=test_booking_data, headers=auth_headers)
    assert response.status_code == 200


def test_create_booking_invalid_times(test_client: TestClient, test_booking_data, auth_headers):
    test_booking_data["end_time"] = "2023-10-01T09:00:00"
    response = test_client.post("/api/v1/bookings/", json=test_booking_data, headers=auth_headers)
    assert response.status_code == 400


def test_read_booking(test_client: TestClient, db_session: Session, test_booking_data, auth_headers):
    response = test_client.post("/api/v1/bookings/", json=test_booking_data, headers=auth_headers)
    booking_id = response.json()["id"]
    response = test_client.get(f"/api/v1/bookings/{booking_id}", headers=auth_headers)
    assert response.status_code == 200


def test_update_booking(test_client: TestClient, db_session: Session, test_booking_data, auth_headers):
    response = test_client.post("/api/v1/bookings/", json=test_booking_data, headers=auth_headers)
    booking_id = response.json()["id"]
    test_booking_data["end_time"] = "2023-10-01T14:00:00"
    response = test_client.put(f"/api/v1/bookings/{booking_id}", json=test_booking_data, headers=auth_headers)
    assert response.status_code == 200


def test_delete_booking(test_client: TestClient, db_session: Session, test_booking_data, auth_headers):
    response = test_client.post("/api/v1/bookings/", json=test_booking_data, headers=auth_headers)
    booking_id = response.json()["id"]
    response = test_client.delete(f"/api/v1/bookings/{booking_id}", headers=auth_headers)
    assert response.status_code == 200
