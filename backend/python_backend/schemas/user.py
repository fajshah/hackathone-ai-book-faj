from pydantic import BaseModel, EmailStr, validator, field_validator
from typing import Optional, List
from datetime import datetime
import re


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    software_experience: Optional[str] = None  # "beginner", "intermediate", "advanced"
    hardware_knowledge: Optional[str] = None  # "none", "basic", "electronics", "robotics", "advanced"
    interests: Optional[List[str]] = []  # ["AI", "Robotics", "Web"]

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v:
            raise ValueError('Username is required')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 50:
            raise ValueError('Username must be at most 50 characters long')
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if v is not None:
            if len(v) > 100:
                raise ValueError('Full name must be at most 100 characters long')
            # Basic validation to ensure name doesn't contain only special characters
            if v.strip() == '':
                raise ValueError('Full name cannot be empty')
        return v

    @field_validator('software_experience')
    @classmethod
    def validate_software_experience(cls, v):
        if v is not None:
            valid_levels = ['beginner', 'intermediate', 'advanced']
            if v not in valid_levels:
                raise ValueError(f'Software experience must be one of: {", ".join(valid_levels)}')
        return v

    @field_validator('hardware_knowledge')
    @classmethod
    def validate_hardware_knowledge(cls, v):
        if v is not None:
            valid_levels = ['none', 'basic', 'electronics', 'robotics', 'advanced']
            if v not in valid_levels:
                raise ValueError(f'Hardware knowledge must be one of: {", ".join(valid_levels)}')
        return v

    @field_validator('interests')
    @classmethod
    def validate_interests(cls, v):
        if v is not None:
            valid_interests = {'AI', 'Web', 'Mobile', 'Embedded', 'Data', 'Robotics'}
            if not isinstance(v, list):
                raise ValueError('Interests must be a list')
            if len(v) > 10:
                raise ValueError('Cannot have more than 10 interests')
            for interest in v:
                if interest not in valid_interests:
                    raise ValueError(f'Interest "{interest}" is not valid. Valid interests are: {", ".join(sorted(valid_interests))}')
            # Remove duplicates while preserving order
            return list(dict.fromkeys(v))
        return v


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 128:
            raise ValueError('Password must be at most 128 characters long')

        # Check for at least one uppercase, one lowercase, one digit, and one special character
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in v)

        if not (has_upper and has_lower and has_digit):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and one digit')

        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    software_experience: Optional[str] = None
    hardware_knowledge: Optional[str] = None
    interests: Optional[List[str]] = None

    @field_validator('full_name', 'email', 'software_experience', 'hardware_knowledge', 'interests', mode='before')
    @classmethod
    def validate_optional_fields(cls, v):
        if v is None:
            return v
        # Apply same validation as UserBase for non-None values
        if hasattr(cls, f'validate_{v.__class__.__name__}'):
            return v
        return v

    @field_validator('full_name', mode='before')
    @classmethod
    def validate_update_full_name(cls, v):
        if v is not None:
            if len(v) > 100:
                raise ValueError('Full name must be at most 100 characters long')
            if v.strip() == '':
                raise ValueError('Full name cannot be empty')
        return v

    @field_validator('software_experience', mode='before')
    @classmethod
    def validate_update_software_experience(cls, v):
        if v is not None:
            valid_levels = ['beginner', 'intermediate', 'advanced']
            if v not in valid_levels:
                raise ValueError(f'Software experience must be one of: {", ".join(valid_levels)}')
        return v

    @field_validator('hardware_knowledge', mode='before')
    @classmethod
    def validate_update_hardware_knowledge(cls, v):
        if v is not None:
            valid_levels = ['none', 'basic', 'electronics', 'robotics', 'advanced']
            if v not in valid_levels:
                raise ValueError(f'Hardware knowledge must be one of: {", ".join(valid_levels)}')
        return v

    @field_validator('interests', mode='before')
    @classmethod
    def validate_update_interests(cls, v):
        if v is not None:
            if not isinstance(v, list):
                raise ValueError('Interests must be a list')
            if len(v) > 10:
                raise ValueError('Cannot have more than 10 interests')
            valid_interests = {'AI', 'Web', 'Mobile', 'Embedded', 'Data', 'Robotics'}
            for interest in v:
                if interest not in valid_interests:
                    raise ValueError(f'Interest "{interest}" is not valid. Valid interests are: {", ".join(sorted(valid_interests))}')
            # Remove duplicates while preserving order
            return list(dict.fromkeys(v))
        return v


class User(UserBase):
    id: int
    email_verified: bool = False
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None