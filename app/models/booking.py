# app/models/booking.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.payments import Payment  # Ensure this import is present


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = {'comment': 'Table to store booking information'}

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    qr_code = Column(String, nullable=True)

    car = relationship("Car", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
    payment = relationship("Payment", back_populates="booking", uselist=False)

    def __repr__(self):
        return f"<Booking {self.id}>"

    def __str__(self):
        return self.__repr__()
