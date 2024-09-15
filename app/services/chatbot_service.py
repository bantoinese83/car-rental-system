# app/services/chatbot_service.py

import ujson
from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from app.crud import crud_booking
from app.crud import crud_car
from app.schemas.booking import BookingCreate
from app.schemas.car import CarInDB


def handle_inquire_rentals(db: Session):
    try:
        logger.debug("Fetching cars from the database")
        cars = crud_car.get_cars(db)
        cars_serialized = [CarInDB.from_orm(car).dict() for car in cars]
        return ujson.dumps({"cars": cars_serialized})
    except Exception as e:
        logger.error(f"Error in handle_inquire_rentals: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def handle_book_rental(db: Session, booking_data: BookingCreate):
    try:
        booking = crud_booking.create_booking(db, booking_data)
        logger.info(f"Booking created with ID: {booking.id}")
        return booking
    except Exception as e:
        logger.error(f"Error in handle_book_rental: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def handle_cancel_booking(db: Session, booking_id: int):
    try:
        booking = crud_booking.delete_booking(db, booking_id)
        if not booking:
            logger.warning(f"Booking with ID {booking_id} not found.")
            raise HTTPException(status_code=404, detail="Booking not found.")
        logger.info(f"Booking with ID {booking_id} cancelled.")
        return booking
    except Exception as e:
        logger.error(f"Error in handle_cancel_booking: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def handle_search_cars(db: Session, search_criteria: dict):
    try:
        cars = crud_car.search_cars(db, search_criteria)
        if not cars:
            logger.warning("No cars found matching the search criteria.")
            raise HTTPException(status_code=404, detail="No cars found matching the search criteria.")
        logger.info(f"Found {len(cars)} cars matching the search criteria.")
        return cars
    except Exception as e:
        logger.error(f"Error in handle_search_cars: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")