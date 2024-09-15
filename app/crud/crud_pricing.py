import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.car import Car
from app.schemas.pricing import PricingCreate, PricingUpdate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_car_pricing(db: Session, car_id: int):
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        if not car:
            logger.warning(f"Car with id {car_id} not found.")
            return None
        return car.base_price
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        return None


def create_pricing(db: Session, pricing: PricingCreate):
    try:
        car = db.query(Car).filter(Car.id == pricing.car_id).first()
        if not car:
            logger.warning(f"Car with id {pricing.car_id} not found.")
            return None
        car.base_price = pricing.surge_price
        db.add(car)
        db.commit()
        db.refresh(car)
        logger.info(f"Pricing created for car id {car.id}.")
        return car
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        db.rollback()
        return None


def update_pricing(db: Session, car_id: int, pricing: PricingUpdate):
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        if not car:
            logger.warning(f"Car with id {car_id} not found.")
            return None
        car.base_price = pricing.surge_price
        db.commit()
        db.refresh(car)
        logger.info(f"Pricing updated for car id {car.id}.")
        return car
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {e}")
        db.rollback()
        return None
