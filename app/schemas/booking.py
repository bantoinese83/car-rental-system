from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class BookingBase(BaseModel):
    car_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    price: float = Field(..., gt=0, description="Price must be greater than zero")

    @field_validator("end_time")
    def end_time_must_be_after_start_time(cls, end_time, values):
        if "start_time" in values and end_time <= values["start_time"]:
            raise ValueError("end_time must be after start_time")
        return end_time


class BookingCreate(BookingBase):
    pass


class BookingInDB(BookingBase):
    id: int

    class Config:
        from_attributes = True


class BookingUpdate(BookingBase):
    pass