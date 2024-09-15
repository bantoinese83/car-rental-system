import asyncio
import secrets
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled exception: {e}")
            response = JSONResponse({"error": str(e)}, status_code=500)
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if
                                    timestamp > current_time - self.window]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(status_code=429, content={"error": "Too many requests"})

        self.requests[client_ip].append(current_time)
        return await call_next(request)


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, timeout: int):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return PlainTextResponse(status_code=504, content="Request timed out")


def init_middlewares(app: FastAPI, middleware_config: dict):
    """
    Initialize middlewares for the FastAPI application based on the provided configuration.

    Args:
        app (FastAPI): The FastAPI application instance.
        middleware_config (dict): Configuration dictionary to enable/disable middlewares.
    """
    if middleware_config.get("cors", True):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Adjust this to your needs
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info("CORS middleware enabled")

    if middleware_config.get("gzip", True):
        app.add_middleware(GZipMiddleware, minimum_size=1000)
        logger.info("GZip middleware enabled")

    if middleware_config.get("session", True):
        app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))
        logger.info("Session middleware enabled")

    if middleware_config.get("trusted_host", True):
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
        logger.info("Trusted host middleware enabled")

    if middleware_config.get("error_handling", True):
        app.add_middleware(ErrorHandlingMiddleware)
        logger.info("Error handling middleware enabled")

    if middleware_config.get("rate_limit", True):
        app.add_middleware(RateLimitMiddleware, max_requests=5, window=60)
        logger.info("Rate limiting middleware enabled")

    if middleware_config.get("timeout", True):
        app.add_middleware(TimeoutMiddleware, timeout=5)
        logger.info("Timeout middleware enabled")

    # Custom exception handler
    @app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"message": "An internal server error occurred."},
        )

    return app
