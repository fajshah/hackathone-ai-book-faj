"""
Authentication configuration module for Better Auth integration
"""
from typing import Optional
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.config import settings
from src.database import SessionLocal
from src.models.user import User
from sqlalchemy.orm import Session
import json


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme for token authentication
security = HTTPBearer()


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(data: dict):
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """Verify a JWT token and return token data"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            return None
        token_data = TokenData(username=username, user_id=user_id)
        return token_data
    except jwt.JWTError:
        return None


def get_current_user(token: str = Depends(security)) -> User:
    """Get the current user from the token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token.credentials)
    if token_data is None:
        raise credentials_exception

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == token_data.user_id).first()
        if user is None:
            raise credentials_exception
        return user
    finally:
        db.close()


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user, ensuring they are active"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_profile_data(profile_data: dict) -> bool:
    """Validate the profile data for background information"""
    # Validate software experience
    software_experience = profile_data.get("software_experience")
    if software_experience and software_experience not in ["beginner", "intermediate", "advanced"]:
        return False

    # Validate hardware knowledge
    hardware_knowledge = profile_data.get("hardware_knowledge")
    if hardware_knowledge and hardware_knowledge not in ["none", "basic", "electronics", "robotics", "advanced"]:
        return False

    # Validate interests
    interests = profile_data.get("interests")
    if interests:
        if not isinstance(interests, list):
            return False
        valid_interests = {"AI", "Web", "Mobile", "Embedded", "Data", "Robotics"}
        if not all(interest in valid_interests for interest in interests):
            return False

    return True


def serialize_interests(interests: list) -> str:
    """Serialize interests list to JSON string"""
    return json.dumps(interests) if interests else "[]"


def deserialize_interests(interests_str: str) -> list:
    """Deserialize interests JSON string to list"""
    try:
        return json.loads(interests_str) if interests_str else []
    except json.JSONDecodeError:
        return []