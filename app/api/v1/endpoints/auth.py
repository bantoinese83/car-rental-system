from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
from sqlalchemy.orm import Session

from app.core.app_config import settings
from app.core.dependencies import get_db_session, get_current_user
from app.core.security import create_access_token, get_password_hash
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserInDB

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db_session)):
    logger.info(f"Attempting to register user with email: {user.email}")
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.error(f"User with email {user.email} already exists.")
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            is_active=user.is_active,
            role=user.role,
            full_name=user.full_name,
            phone_number=user.phone_number
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User registered successfully: {user.email}")
        return {"message": "User registered successfully", "id": db_user.id}
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Attempting to log in user with email: {form_data.username}")
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not crud_user.verify_user_password(user, form_data.password):
        logger.warning(f"Login failed: Incorrect username or password for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        logger.info(f"User logged in successfully with email: {form_data.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user
