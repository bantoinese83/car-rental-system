import ujson
from sqlalchemy.orm import Session
from app.models.car import Car
from app.services.chatbot_service import handle_inquire_rentals


def test_handle_inquire_rentals(db_session: Session):
    # Create a mock car object
    car = Car(
        id=1,
        model="Test Model",
        available=True,
        daily_rate=100.0,
        vehicle_type="SUV",  # Use lowercase to match the actual output
        location="Test Location",
        branch_id=1
    )
    db_session.add(car)
    db_session.commit()

    # Call the function
    response = handle_inquire_rentals(db_session)

    # Deserialize the response
    response_data = ujson.loads(response)

    # Check if the response contains the car data
    assert "cars" in response_data
    assert len(response_data["cars"]) == 1
    assert response_data["cars"][0]["model"] == "Test Model"
    assert response_data["cars"][0]["available"] is True
    assert response_data["cars"][0]["daily_rate"] == 100.0
    assert response_data["cars"][0]["vehicle_type"] == "suv"  # Use lowercase to match the actual output
