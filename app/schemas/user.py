from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    role: Role


class UserCreate(UserBase):
    username: str = Field(..., min_length=1, max_length=50,
                          description="Username must be between 1 and 50 characters long")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    role: Role = Role.USER
    full_name: str = Field(None, max_length=100, description="Full name must be less than 100 characters long")
    phone_number: str = Field(None, max_length=15, description="Phone number must be less than 15 characters long")


class UserInDB(UserBase):
    id: int
    is_active: bool = Field(default=True)
    role: Role

    class Config:
        from_attributes = True


class UserUpdate(UserBase):
    username: str = Field(None, min_length=1, max_length=50,
                          description="Username must be between 1 and 50 characters long")
    password: str = Field(None, min_length=8, description="Password must be at least 8 characters long")
    role: Role = Field(None)
    full_name: str = Field(None, max_length=100, description="Full name must be less than 100 characters long")
    phone_number: str = Field(None, max_length=15, description="Phone number must be less than 15 characters long")
    is_active: bool = Field(None)