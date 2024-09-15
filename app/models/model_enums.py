from enum import Enum
from enum import Enum as PyEnum


class VehicleType(PyEnum):
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


class STATUS(PyEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
