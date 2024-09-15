from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session, get_current_active_user, get_current_active_admin
from app.crud import crud_pricing
from app.schemas.pricing import PricingResponse, PricingCreate, PricingUpdate

router = APIRouter()


@router.get("/pricing", response_model=PricingResponse, dependencies=[Depends(get_current_active_user)])
async def get_pricing(car_id: int, db: Session = Depends(get_db_session)):
    try:
        pricing = crud_pricing.get_car_pricing(db=db, car_id=car_id)
        if not pricing:
            logger.warning(f"Car not found: {car_id}")
            raise HTTPException(status_code=404, detail="Car not found")
        logger.info(f"Pricing retrieved for car: {car_id}")
        return pricing
    except Exception as e:
        logger.error(f"Error retrieving pricing: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/pricing", response_model=PricingResponse, dependencies=[Depends(get_current_active_admin)])
async def create_pricing(pricing: PricingCreate, db: Session = Depends(get_db_session)):
    try:
        new_pricing = crud_pricing.create_pricing(db=db, pricing=pricing)
        logger.info(f"Pricing created for car: {new_pricing.car_id}")
        return new_pricing
    except Exception as e:
        logger.error(f"Error creating pricing: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/pricing/{car_id}", response_model=PricingResponse, dependencies=[Depends(get_current_active_admin)])
async def update_pricing(car_id: int, pricing: PricingUpdate, db: Session = Depends(get_db_session)):
    try:
        updated_pricing = crud_pricing.update_pricing(db=db, car_id=car_id, pricing=pricing)
        if not updated_pricing:
            logger.warning(f"Car not found: {car_id}")
            raise HTTPException(status_code=404, detail="Car not found")
        logger.info(f"Pricing updated for car: {car_id}")
        return updated_pricing
    except Exception as e:
        logger.error(f"Error updating pricing: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
