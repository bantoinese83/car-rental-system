from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.model_enums import STATUS


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = {'comment': 'Table to store payment information'}

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, index=True)
    status = Column(Enum(STATUS), default=STATUS.PENDING, nullable=False)
    amount = Column(Float, nullable=False)
    reference = Column(String, nullable=True)

    booking = relationship("Booking", back_populates="payment")

    def __repr__(self):
        return f"<Payment {self.id}>"

    def __str__(self):
        return self.__repr__()
