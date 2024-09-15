from pydantic import BaseModel, Field


class PricingBase(BaseModel):
    car_id: int
    surge_price: float = Field(..., gt=0, description="Surge price must be greater than zero")


class PricingResponse(PricingBase):
    class Config:
        from_attributes = True


class PricingCreate(PricingBase):
    pass


class PricingUpdate(BaseModel):
    surge_price: float = Field(..., gt=0, description="Surge price must be greater than zero")
