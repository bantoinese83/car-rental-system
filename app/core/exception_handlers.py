# app/core/exception_handlers.py
import stripe
from fastapi import Request, HTTPException
from fastapi.responses import UJSONResponse, JSONResponse
from loguru import logger


async def exception_handler(request: Request, exc: Exception):
    if isinstance(exc, stripe.error.StripeError):
        return UJSONResponse(status_code=400, content={"detail": str(exc)})
    if isinstance(exc, HTTPException):
        return UJSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    return UJSONResponse(status_code=500, content={"detail": "Internal server error"})


async def custom_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )
