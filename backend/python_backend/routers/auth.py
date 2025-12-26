from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.user import User as UserModel
from schemas.user import UserCreate, User, Token, UserUpdate
from utils.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_current_active_user
)
from config import settings
from services.validation_service import ValidationService
import json
from typing import Optional, List


router = APIRouter(prefix="/api/auth", tags=["authentication"])


def serialize_interests(interests: List[str]) -> str:
    """Serialize interests list to JSON string"""
    return json.dumps(interests) if interests else "[]"


def deserialize_interests(interests_str: Optional[str]) -> List[str]:
    """Deserialize interests JSON string to list"""
    try:
        return json.loads(interests_str) if interests_str else []
    except (json.JSONDecodeError, TypeError):
        return []


@router.post("/signup", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with profile information"""
    # Initialize validation service
    validation_service = ValidationService()

    # Perform comprehensive validation
    validation_result = validation_service.validate_user_registration({
        'email': user.email,
        'username': user.username,
        'password': user.password,
        'software_experience': user.software_experience,
        'hardware_knowledge': user.hardware_knowledge,
        'interests': user.interests
    })

    if not validation_result['is_valid']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation failed: {'; '.join(validation_result['errors'])}"
        )

    # Check if user already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Sanitize and validate inputs
    sanitized_username = validation_service.sanitize_input(user.username)
    sanitized_full_name = validation_service.sanitize_input(user.full_name) if user.full_name else None

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user with profile fields
    db_user = UserModel(
        username=sanitized_username,
        email=user.email,
        full_name=sanitized_full_name,
        hashed_password=hashed_password,
        software_experience=user.software_experience,
        hardware_knowledge=user.hardware_knowledge,
        interests=serialize_interests(user.interests) if user.interests else None,
        email_verified=False  # Email verification would happen separately
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Update the response to include profile fields
    db_user.interests = deserialize_interests(db_user.interests)
    return db_user


@router.post("/signin", response_model=Token)
async def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user with email and password"""
    # In FastAPI's OAuth2PasswordRequestForm, the 'username' field is used for email
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive account",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time
    user.last_login_at = func.now()
    db.commit()

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id}, expires_delta=access_token_expires
    )

    # Create refresh token
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = create_refresh_token(
        data={"sub": user.username, "user_id": user.id}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@router.post("/login", response_model=Token)  # Keep the old endpoint for compatibility
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and return access token (alias for signin)"""
    return await signin(form_data, db)


@router.post("/signout")
async def signout():
    """Sign out current user (client-side token removal)"""
    return {"success": True, "message": "Successfully signed out"}


@router.post("/refresh")
async def refresh_token(token: str, db: Session = Depends(get_db)):
    """Refresh the access token using refresh token"""
    from jose import jwt
    from utils.auth import SECRET_KEY, ALGORITHM
    from schemas.user import Token
    from sqlalchemy import func

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


@router.get("/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    """Get current user details"""
    # Deserialize interests for the response
    current_user.interests = deserialize_interests(current_user.interests)
    return current_user


@router.put("/profile", response_model=User)
async def update_profile(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user profile information"""
    # Initialize validation service
    validation_service = ValidationService()

    # Validate update data
    update_data = {}
    if user_update.full_name is not None:
        update_data['full_name'] = user_update.full_name
    if user_update.software_experience is not None:
        update_data['software_experience'] = user_update.software_experience
    if user_update.hardware_knowledge is not None:
        update_data['hardware_knowledge'] = user_update.hardware_knowledge
    if user_update.interests is not None:
        update_data['interests'] = user_update.interests

    validation_result = validation_service.validate_user_update(update_data)
    if not validation_result['is_valid']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation failed: {'; '.join(validation_result['errors'])}"
        )

    # Update fields if provided
    if user_update.full_name is not None:
        sanitized_full_name = validation_service.sanitize_input(user_update.full_name)
        current_user.full_name = sanitized_full_name
    if user_update.email is not None:
        # Check if email is already taken by another user
        existing_user = db.query(UserModel).filter(
            UserModel.email == user_update.email,
            UserModel.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered by another user"
            )
        current_user.email = user_update.email
    if user_update.is_active is not None:
        current_user.is_active = user_update.is_active
    if user_update.software_experience is not None:
        current_user.software_experience = user_update.software_experience
    if user_update.hardware_knowledge is not None:
        current_user.hardware_knowledge = user_update.hardware_knowledge
    if user_update.interests is not None:
        current_user.interests = serialize_interests(user_update.interests)

    db.commit()
    db.refresh(current_user)

    # Deserialize interests for the response
    current_user.interests = deserialize_interests(current_user.interests)
    return current_user