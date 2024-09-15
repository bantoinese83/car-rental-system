from sqlalchemy import Column, Integer, Float, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.model_enums import VehicleType


class Car(Base):
    __tablename__ = "cars"
    __table_args__ = {'comment': 'Table to store car information'}

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    available = Column(Boolean, default=True)
    daily_rate = Column(Float, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    location = Column(String, nullable=True)
    branch_id = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="car")

    def __repr__(self):
        return f"<Car {self.id}>"

    def __str__(self):
        return self.__repr__()
