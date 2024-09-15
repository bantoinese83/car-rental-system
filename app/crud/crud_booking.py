from io import BytesIO

import qrcode
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingUpdate


def get_booking(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()


def get_bookings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Booking).offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BookingCreate):
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # Generate QR code
    qr_data = f"Booking ID: {db_booking.id}, Car ID: {db_booking.car_id}, User ID: {db_booking.user_id}, Start Time: {db_booking.start_time}, End Time: {db_booking.end_time}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_image = buffer.getvalue()

    # Assuming you have a field in Booking model to store QR code image
    db_booking.qr_code = qr_code_image
    db.commit()
    db.refresh(db_booking)

    return db_booking


def update_booking(db: Session, booking_id: int, booking: BookingUpdate):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        for key, value in booking.dict(exclude_unset=True).items():
            setattr(db_booking, key, value)
        db.commit()
        db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking
