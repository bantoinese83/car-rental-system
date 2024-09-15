from sqlalchemy.orm import Session

from app.models.car import Car
from app.schemas.car import CarCreate, CarUpdate, CarInDB
from app.utils.cache import get_cache, set_cache, delete_cache


def get_car(db: Session, car_id: int):
    cache_key = f"car_{car_id}"
    cached_car = get_cache(cache_key)
    if cached_car:
        return cached_car

    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car:
        set_cache(cache_key, db_car)
    return db_car


def get_cars(db: Session, skip: int = 0, limit: int = 10):
    cache_key = f"cars_{skip}_{limit}"
    cached_cars = get_cache(cache_key)
    if cached_cars:
        return [CarInDB(**car) for car in cached_cars]

    db_cars = db.query(Car).offset(skip).limit(limit).all()
    db_cars_dict = [CarInDB.from_orm(car).dict() for car in db_cars]
    set_cache(cache_key, db_cars_dict)
    return db_cars

    db_cars = db.query(Car).offset(skip).limit(limit).all()
    set_cache(cache_key, db_cars)
    return db_cars


def create_car(db: Session, car: CarCreate):
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    delete_cache("cars_*")  # Invalidate the cache for car lists
    return db_car


def update_car(db: Session, car_id: int, car: CarUpdate):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car:
        for key, value in car.dict(exclude_unset=True).items():
            setattr(db_car, key, value)
        db.commit()
        db.refresh(db_car)
        delete_cache(f"car_{car_id}")  # Invalidate the cache for this car
        delete_cache("cars_*")  # Invalidate the cache for car lists
    return db_car


def delete_car(db: Session, car_id: int):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car:
        db.delete(db_car)
        db.commit()
        delete_cache(f"car_{car_id}")  # Invalidate the cache for this car
        delete_cache("cars_*")  # Invalidate the cache for car lists
    return db_car


def search_cars(db: Session, search_criteria: dict, skip: int = 0, limit: int = 10):
    cache_key = f"search_cars_{str(search_criteria)}_{skip}_{limit}"
    cached_cars = get_cache(cache_key)
    if cached_cars:
        return cached_cars

    query = db.query(Car)
    if 'model' in search_criteria:
        query = query.filter(Car.model.ilike(f"%{search_criteria['model']}%"))
    if 'available' in search_criteria:
        query = query.filter(Car.available == search_criteria['available'])
    if 'min_price' in search_criteria:
        query = query.filter(Car.base_price >= search_criteria['min_price'])
    if 'max_price' in search_criteria:
        query = query.filter(Car.base_price <= search_criteria['max_price'])
    if 'vehicle_type' in search_criteria:
        query = query.filter(Car.vehicle_type == search_criteria['vehicle_type'])
    if 'location' in search_criteria:
        query = query.filter(Car.location.ilike(f"%{search_criteria['location']}%"))
    if 'daily_rate' in search_criteria:
        query = query.filter(Car.daily_rate == search_criteria['daily_rate'])

    db_cars = query.offset(skip).limit(limit).all()
    # Assuming db_cars is a list of car objects
    db_cars_dict: dict = {car.id: car.__dict__ for car in db_cars}
    set_cache(cache_key, db_cars_dict)
    return db_cars
