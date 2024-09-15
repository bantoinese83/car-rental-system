from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session, get_current_active_user, get_current_active_admin
from app.crud import crud_car
from app.schemas.car import CarCreate, CarInDB, CarUpdate

router = APIRouter()


@router.post("/", response_model=CarInDB, dependencies=[Depends(get_current_active_admin)])
async def create_car(car: CarCreate, db: Session = Depends(get_db_session)):
    try:
        new_car = crud_car.create_car(db=db, car=car)
        logger.info(f"Car created: {new_car.id}")
        return new_car
    except Exception as e:
        logger.error(f"Error creating car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{car_id}", response_model=CarInDB, dependencies=[Depends(get_current_active_user)])
async def read_car(car_id: int, db: Session = Depends(get_db_session)):
    try:
        car = crud_car.get_car(db=db, car_id=car_id)
        if car is None:
            logger.warning(f"Car not found: {car_id}")
            raise HTTPException(status_code=404, detail="Car not found")
        logger.info(f"Car retrieved: {car.id}")
        return car
    except Exception as e:
        logger.error(f"Error retrieving car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/{car_id}", response_model=CarInDB, dependencies=[Depends(get_current_active_admin)])
async def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db_session)):
    try:
        updated_car = crud_car.update_car(db=db, car_id=car_id, car=car)
        if updated_car is None:
            logger.warning(f"Car not found: {car_id}")
            raise HTTPException(status_code=404, detail="Car not found")
        logger.info(f"Car updated: {updated_car.id}")
        return updated_car
    except Exception as e:
        logger.error(f"Error updating car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{car_id}", response_model=CarInDB, dependencies=[Depends(get_current_active_admin)])
async def delete_car(car_id: int, db: Session = Depends(get_db_session)):
    try:
        deleted_car = crud_car.delete_car(db=db, car_id=car_id)
        if deleted_car is None:
            logger.warning(f"Car not found: {car_id}")
            raise HTTPException(status_code=404, detail="Car not found")
        logger.info(f"Car deleted: {car_id}")
        return deleted_car
    except Exception as e:
        logger.error(f"Error deleting car: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/", response_model=List[CarInDB], dependencies=[Depends(get_current_active_user)])
async def search_cars(
        db: Session = Depends(get_db_session),
        model: Optional[str] = Query(None, description="Filter by car model"),
        available: Optional[bool] = Query(None, description="Filter by availability"),
        min_price: Optional[float] = Query(None, description="Filter by minimum price"),
        max_price: Optional[float] = Query(None, description="Filter by maximum price"),
        vehicle_type: Optional[str] = Query(None, description="Filter by vehicle type"),
        location: Optional[str] = Query(None, description="Filter by location"),
        daily_rate: Optional[float] = Query(None, description="Filter by daily rate"),
        skip: int = Query(0, description="Number of records to skip for pagination"),
        limit: int = Query(10, description="Maximum number of records to return")
):
    try:
        search_criteria = {
            "model": model,
            "available": available,
            "min_price": min_price,
            "max_price": max_price,
            "vehicle_type": vehicle_type,
            "location": location,
            "daily_rate": daily_rate
        }
        cars = crud_car.search_cars(db=db, search_criteria=search_criteria, skip=skip, limit=limit)
        logger.info(f"Found {len(cars)} cars matching the search criteria")
        return cars
    except Exception as e:
        logger.error(f"Error searching cars: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
