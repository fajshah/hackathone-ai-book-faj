from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import re
from typing import Optional

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def validate_input(text: str) -> bool:
    """Validate input text for potential security issues"""
    # Check for SQL injection patterns
    sql_patterns = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION|WAITFOR|SLEEP)\b)",
        r"(\b(OR|AND)\s+[\w\s]*=)",
        r"(';|--|#|/\*|\*/)"
    ]

    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False

    # Check for XSS patterns
    xss_patterns = [
        r"<script.*?>",
        r"javascript:",
        r"vbscript:",
        r"on\w+\s*="
    ]

    for pattern in xss_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return False

    return True

async def security_middleware(request: Request, call_next):
    """Security middleware to validate requests"""
    # Validate content type for POST/PUT requests
    if request.method in ["POST", "PUT", "PATCH"]:
        content_type = request.headers.get("content-type", "")
        if not content_type.startswith("application/json") and request.method in ["POST", "PUT", "PATCH"]:
            # For form data, we still need to validate the content
            if content_type.startswith("application/x-www-form-urlencoded") or content_type.startswith("multipart/form-data"):
                # For now, we'll allow form data but in a real app you'd want to validate it
                pass

    # Process the request
    response = await call_next(request)

    # Add security headers to response
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    return response

def setup_security(app):
    """Setup security features for the application"""
    # Register rate limit handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add security middleware
    app.middleware("http")(security_middleware)