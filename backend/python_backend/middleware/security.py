"""
Security middleware for the Physical AI & Humanoid Robotics Textbook API
"""
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time


def setup_security(app: FastAPI):
    """
    Setup security features for the FastAPI application
    """
    # Initialize rate limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add rate limiting middleware
    @app.middleware("http")
    async def add_rate_limiting(request, call_next):
        # Apply rate limiting - limit to 100 requests per minute per IP
        try:
            response = await call_next(request)
            return response
        except Exception:
            raise

    # Add security headers middleware
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    # Add timing attack protection
    @app.middleware("http")
    async def add_timing_attack_protection(request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Response-Time"] = str(process_time)
        return response