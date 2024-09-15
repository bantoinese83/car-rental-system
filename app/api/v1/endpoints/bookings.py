from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session, get_current_active_user
from app.crud import crud_booking
from app.schemas.booking import BookingCreate, BookingInDB, BookingUpdate

router = APIRouter()


@router.post("/", response_model=BookingInDB, dependencies=[Depends(get_current_active_user)])
async def create_booking(booking: BookingCreate, db: Session = Depends(get_db_session)):
    try:
        if booking.start_time >= booking.end_time:
            logger.warning("Invalid booking times: start_time must be before end_time")
            raise HTTPException(status_code=400, detail="Invalid booking times: start_time must be before end_time")

        # Create the booking
        new_booking = crud_booking.create_booking(db=db, booking=booking)
        logger.info(f"Booking created: {new_booking.id}")
        return new_booking
    except HTTPException as e:
        logger.error(f"HTTP error creating booking: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating booking: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{booking_id}", response_model=BookingInDB, dependencies=[Depends(get_current_active_user)])
async def read_booking(booking_id: int, db: Session = Depends(get_db_session)):
    try:
        booking = crud_booking.get_booking(db=db, booking_id=booking_id)
        if booking is None:
            logger.warning(f"Booking not found: {booking_id}")
            raise HTTPException(status_code=404, detail="Booking not found")
        logger.info(f"Booking retrieved: {booking.id}")
        return booking
    except Exception as e:
        logger.error(f"Error retrieving booking: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{booking_id}", response_model=BookingInDB, dependencies=[Depends(get_current_active_user)])
async def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db_session)):
    try:
        updated_booking = crud_booking.update_booking(db=db, booking_id=booking_id, booking=booking)
        if updated_booking is None:
            logger.warning(f"Booking not found: {booking_id}")
            raise HTTPException(status_code=404, detail="Booking not found")
        logger.info(f"Booking updated: {updated_booking.id}")
        return updated_booking
    except Exception as e:
        logger.error(f"Error updating booking: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{booking_id}", response_model=BookingInDB, dependencies=[Depends(get_current_active_user)])
async def delete_booking(booking_id: int, db: Session = Depends(get_db_session)):
    try:
        deleted_booking = crud_booking.delete_booking(db=db, booking_id=booking_id)
        if deleted_booking is None:
            logger.warning(f"Booking not found: {booking_id}")
            raise HTTPException(status_code=404, detail="Booking not found")
        logger.info(f"Booking deleted: {booking_id}")
        return deleted_booking
    except Exception as e:
        logger.error(f"Error deleting booking: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")