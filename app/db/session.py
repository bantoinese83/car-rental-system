import logging

from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

from app.core.app_config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine with a connection pool
try:
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,  # Adjust the pool size as needed
        max_overflow=20,  # Adjust the max overflow as needed
        pool_pre_ping=True
    )
    logger.info("Database engine created successfully with connection pool.")
except exc.SQLAlchemyError as e:
    logger.error(f"Error creating database engine: {e}")
    raise

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except exc.SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        raise
    finally:
        db.close()
        logger.info("Database session closed.")


def get_engine():
    return engine