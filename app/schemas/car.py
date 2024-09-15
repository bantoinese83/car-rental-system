from enum import Enum

from pydantic import BaseModel, Field


class VehicleType(str, Enum):
    SUV = "suv"
    LUXURY = "luxury"
    SEDAN = "sedan"
    TRUCK = "truck"
    COUPE = "coupe"
    HATCHBACK = "hatchback"
    CONVERTIBLE = "convertible"
    WAGON = "wagon"
    VAN = "van"
    MINIVAN = "minivan"
    PICKUP = "pickup"
    SPORTS_CAR = "sports_car"


class CarBase(BaseModel):
    model: str = Field(..., min_length=1, max_length=100)
    available: bool = Field(default=True)
    daily_rate: float = Field(..., gt=0, description="Base price must be greater than zero")
    vehicle_type: VehicleType = Field(..., description="The type of the vehicle")
    location: str = Field(None, description="Location of the vehicle")
    branch_id: int = Field(..., description="Branch ID")


class CarCreate(CarBase):
    pass


class CarInDB(CarBase):
    id: int

    class Config:
        from_attributes = True


class CarUpdate(CarBase):
    pass
