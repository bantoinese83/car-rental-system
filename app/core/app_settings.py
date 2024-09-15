# app/core/app_settings.py
from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GOOGLE_API_KEY: str
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    REDIS_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
