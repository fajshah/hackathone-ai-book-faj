from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, User, Token
from src.utils.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_current_active_user
)
from src.config import settings

router = APIRouter(tags=["authentication"])

@router.post("/auth/signup", response_model=User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and return access token"""
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Create refresh token
    refresh_token_expires = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@router.post("/auth/refresh")
async def refresh_token(token: str, db: Session = Depends(get_db)):
    """Refresh the access token using refresh token"""
    from jose import jwt
    from src.utils.auth import SECRET_KEY, ALGORITHM
    from src.schemas.user import Token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type: str = payload.get("type")

        if username is None or token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        # Create new access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
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


@router.get("/auth/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user details"""
    return current_user