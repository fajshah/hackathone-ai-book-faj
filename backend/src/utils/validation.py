from typing import Optional
import re
from pydantic import BaseModel, validator, field_validator
from fastapi import HTTPException, status


def validate_username(username: str) -> str:
    """Validate username format"""
    if not username or len(username) < 3 or len(username) > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be between 3 and 50 characters"
        )

    if not re.match("^[a-zA-Z0-9_]+$", username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username can only contain letters, numbers, and underscores"
        )

    return username


def validate_email(email: str) -> str:
    """Validate email format"""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    return email


def validate_password(password: str) -> str:
    """Validate password strength"""
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )

    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter"
        )

    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one digit"
        )

    return password


def sanitize_text(text: str) -> str:
    """Sanitize text input to prevent XSS and other injection attacks"""
    if not text:
        return text

    # Remove potentially dangerous characters/sequences
    sanitized = text.replace("<script", "&lt;script")
    sanitized = sanitized.replace("javascript:", "javascript&#58;")
    sanitized = sanitized.replace("vbscript:", "vbscript&#58;")
    sanitized = sanitized.replace("onerror", "onerror_")
    sanitized = sanitized.replace("onload", "onload_")

    return sanitized


def validate_content_length(content: str, max_length: int = 10000) -> str:
    """Validate content length"""
    if len(content) > max_length:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content exceeds maximum length of {max_length} characters"
        )
    return content