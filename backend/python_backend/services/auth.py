"""
Authentication service for Better Auth integration
Handles user registration, login, profile management, and session handling
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
import json

from models.user import User
from config.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    validate_profile_data,
    serialize_interests,
    deserialize_interests
)
from config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(
        self,
        email: str,
        password: str,
        username: str,
        full_name: Optional[str] = None,
        software_experience: Optional[str] = None,
        hardware_knowledge: Optional[str] = None,
        interests: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Register a new user with profile information
        """
        # Validate profile data if provided
        if software_experience or hardware_knowledge or interests:
            profile_data = {
                "software_experience": software_experience,
                "hardware_knowledge": hardware_knowledge,
                "interests": interests
            }
            if not validate_profile_data(profile_data):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid profile data provided"
                )

        # Check if user already exists
        existing_user = self.db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            if existing_user.email == email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered"
                )
            if existing_user.username == username:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already taken"
                )

        # Validate password strength
        if len(password) < settings.auth_password_min_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password must be at least {settings.auth_password_min_length} characters long"
            )

        # Hash the password
        hashed_password = get_password_hash(password)

        # Create the user
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
            software_experience=software_experience,
            hardware_knowledge=hardware_knowledge,
            interests=serialize_interests(interests) if interests else None,
            email_verified=False  # Email verification would happen separately
        )

        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )

        # Create tokens
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})

        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "email_verified": user.email_verified,
                "software_experience": user.software_experience,
                "hardware_knowledge": user.hardware_knowledge,
                "interests": deserialize_interests(user.interests) if user.interests else [],
                "created_at": user.created_at.isoformat() if user.created_at else None
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password
        """
        user = self.db.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive account"
            )

        # Update last login time
        user.last_login_at = datetime.utcnow()
        self.db.commit()

        # Create tokens
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        refresh_token = create_refresh_token(data={"sub": user.username, "user_id": user.id})

        return {
            "success": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "email_verified": user.email_verified,
                "software_experience": user.software_experience,
                "hardware_knowledge": user.hardware_knowledge,
                "interests": deserialize_interests(user.interests) if user.interests else [],
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def get_current_user(self, user_id: int) -> Dict[str, Any]:
        """
        Get current user profile
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "email_verified": user.email_verified,
            "software_experience": user.software_experience,
            "hardware_knowledge": user.hardware_knowledge,
            "interests": deserialize_interests(user.interests) if user.interests else [],
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
        }

    def update_user_profile(
        self,
        user_id: int,
        software_experience: Optional[str] = None,
        hardware_knowledge: Optional[str] = None,
        interests: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update user profile information
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Validate profile data if provided
        if software_experience or hardware_knowledge or interests:
            profile_data = {
                "software_experience": software_experience or user.software_experience,
                "hardware_knowledge": hardware_knowledge or user.hardware_knowledge,
                "interests": interests or deserialize_interests(user.interests) if user.interests else []
            }
            if not validate_profile_data(profile_data):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid profile data provided"
                )

        # Update fields if provided
        if software_experience is not None:
            user.software_experience = software_experience
        if hardware_knowledge is not None:
            user.hardware_knowledge = hardware_knowledge
        if interests is not None:
            user.interests = serialize_interests(interests)

        self.db.commit()
        self.db.refresh(user)

        return {
            "success": True,
            "profile": {
                "software_experience": user.software_experience,
                "hardware_knowledge": user.hardware_knowledge,
                "interests": deserialize_interests(user.interests) if user.interests else []
            }
        }

    def get_personalized_content(self, user_id: int) -> Dict[str, Any]:
        """
        Get personalized content recommendations based on user profile
        """
        user = self.db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # This is a placeholder for the actual content personalization logic
        # In a real implementation, this would query content based on user profile
        recommendations = {
            "by_experience": user.software_experience or "beginner",
            "by_interests": deserialize_interests(user.interests) if user.interests else [],
            "by_knowledge": user.hardware_knowledge or "none",
            "recommended_content": [
                "Getting Started with AI",
                "Introduction to Robotics",
                "Python Programming Basics"
            ]
        }

        return {
            "user_id": user.id,
            "recommendations": recommendations
        }