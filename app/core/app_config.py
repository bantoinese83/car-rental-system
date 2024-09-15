import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings, PostgresDsn, validator
from rich.console import Console
from rich.table import Table
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from app.core.app_settings import settings

load_dotenv()

Base = declarative_base()


class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # API Key Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")

    @validator("DATABASE_URL", pre=True)
    def validate_database_url(cls, v: str) -> str:
        if not v:
            raise ValueError("DATABASE_URL must be provided")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        arbitrary_types_allowed = True


console = Console()


def log_settings():
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="dim", width=30)
    table.add_column("Value")

    for key, value in settings.dict().items():
        table.add_row(key, str(value))

    console.print(table)


def get_engine():
    from app.db.session import engine
    return engine


def log_database_tables():
    engine = get_engine()
    inspector = inspect(engine)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Table", style="dim", width=30)
    table.add_column("Columns")

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        column_names = ", ".join([column["name"] for column in columns])
        table.add_row(table_name, column_names)

    console.print(table)


def log_router(app):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Route", style="dim", width=30)
    table.add_column("Methods")
    table.add_column("Name")

    for route in app.routes:
        methods = ", ".join(route.methods)
        table.add_row(route.path, methods, route.name)

    console.print(table)
