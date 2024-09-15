import logging

from fastapi import FastAPI
from progress.spinner import MoonSpinner
from starlette.responses import RedirectResponse

from app.api.v1.endpoints import auth, cars, bookings, pricing, payments, users, agent
from app.core.app_config import log_settings, log_router, log_database_tables
from app.core.exception_handlers import custom_exception_handler
from app.core.middlewares import init_middlewares
from app.core.redis_config import init_redis, get_redis, close_redis
from app.db.session import engine, Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Logging configured successfully.")

app = FastAPI(
    title="Car Rental API 🚗",
    description="A simple API for car rental services using FastAPI. 🏎️",
    version="0.1.0",
)
logger.info("FastAPI application created successfully.")

# Register exception handlers
app.add_exception_handler(Exception, custom_exception_handler)

# Initialize middlewares
middleware_config = {
    "cors": True,
    "gzip": True,
    "session": True,
    "trusted_host": True,
    "error_handling": True,
    "rate_limit": False,
    "timeout": True,
}

init_middlewares(app, middleware_config)
logger.info("Middlewares initialized successfully.")


# Initialize Redis
@app.on_event("startup")
async def on_startup():
    spinner = MoonSpinner('Initializing ')
    try:
        spinner.next()
        await init_redis()
        logger.info("Redis initialized successfully.")
        spinner.next()
        Base.metadata.create_all(bind=engine)
        log_database_tables()
        logger.info("All tables created successfully.")
        spinner.next()
        log_settings()
        logger.info("Application settings logged successfully.")
        spinner.next()
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        spinner.finish()


# Close Redis connection
@app.on_event("shutdown")
async def on_shutdown():
    try:
        await close_redis()
        logger.info("Redis connection closed successfully.")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        raise


# Redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["🏥 Health"])
async def health():
    return {"status": "ok"}


@app.get("/redis", tags=["🏥 Health"])
async def redis():
    redis_health = await get_redis()
    return {"status": "ok", "redis": str(redis_health)}


app.include_router(auth.router, prefix="/api/v1/auth", tags=["🔐 Authentication 🔑"])
app.include_router(cars.router, prefix="/api/v1/cars", tags=["🚗 Cars 🚙"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["📅 Bookings 📆"])
app.include_router(pricing.router, prefix="/api/v1/pricing", tags=["💲 Pricing 💵"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["💳 Payments 💰"])
app.include_router(users.router, prefix="/api/v1/users", tags=["👥 Users 🧑‍🤝‍🧑"])
app.include_router(agent.gemini_router, prefix="/api/v1/agent", tags=["🤖 Agent 🕵️‍♂️"])

# Log routes after including routers
log_router(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
