from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.orm import Session

from app.core.dependencies import get_db_session, get_current_active_admin, get_current_active_user
from app.crud import crud_user
from app.schemas.user import UserInDB, UserUpdate

router = APIRouter()

@router.get("/", response_model=list[UserInDB], dependencies=[Depends(get_current_active_admin)])
async def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_session)):
    try:
        users = crud_user.get_users(db=db, skip=skip, limit=limit)
        logger.info("Users retrieved successfully")
        return users
    except Exception as e:
        logger.error(f"Error retrieving users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/me", response_model=UserInDB, dependencies=[Depends(get_current_active_user)])
async def get_current_user_info(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user

@router.get("/{user_id}", response_model=UserInDB, dependencies=[Depends(get_current_active_admin)])
async def get_user(user_id: int, db: Session = Depends(get_db_session)):
    try:
        user = crud_user.get_user(db=db, user_id=user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"User retrieved: {user_id}")
        return user
    except Exception as e:
        logger.error(f"Error retrieving user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/{user_id}", response_model=UserInDB, dependencies=[Depends(get_current_active_admin)])
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db_session)):
    try:
        updated_user = crud_user.update_user(db=db, user_id=user_id, user=user)
        if not updated_user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"User updated: {user_id}")
        return updated_user
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/{user_id}", response_model=UserInDB, dependencies=[Depends(get_current_active_admin)])
async def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    try:
        deleted_user = crud_user.delete_user(db=db, user_id=user_id)
        if not deleted_user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"User deleted: {user_id}")
        return deleted_user
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")