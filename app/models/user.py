from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.model_enums import Role


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'comment': 'Table to store user information'}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)

    bookings = relationship("Booking", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return self.__repr__()
