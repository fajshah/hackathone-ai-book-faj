"""
Security and validation service for user data and authentication
"""
from typing import Dict, Any, List
from datetime import datetime
import re
import secrets
from passlib.context import CryptContext


class ValidationService:
    """
    Service for validating user input and securing user data
    """

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        self.username_pattern = re.compile(r'^[a-zA-Z0-9_]+$')

        # Blacklisted passwords (commonly used or compromised)
        self.blacklisted_passwords = {
            'password', '12345678', 'qwerty123', 'admin123', 'letmein',
            'welcome', 'monkey', '1234567890', 'abc123', 'password1'
        }

    def validate_email(self, email: str) -> bool:
        """
        Validate email format
        """
        return bool(self.email_pattern.match(email))

    def validate_username(self, username: str) -> bool:
        """
        Validate username format and length
        """
        if len(username) < 3 or len(username) > 50:
            return False
        return bool(self.username_pattern.match(username))

    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Validate password strength and return validation details
        """
        errors = []
        warnings = []

        # Length check
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        elif len(password) > 128:
            errors.append("Password must be at most 128 characters long")

        # Character variety check
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if not has_upper:
            errors.append("Password must contain at least one uppercase letter")
        if not has_lower:
            errors.append("Password must contain at least one lowercase letter")
        if not has_digit:
            errors.append("Password must contain at least one digit")

        # Check against blacklisted passwords
        if password.lower() in self.blacklisted_passwords:
            errors.append("Password is too common and not allowed")

        # Check for common patterns
        if re.search(r'(.)\1{2,}', password):  # Repeated characters
            warnings.append("Password contains repeated characters")

        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            warnings.append("Password contains sequential numbers")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "has_upper": has_upper,
            "has_lower": has_lower,
            "has_digit": has_digit,
            "has_special": has_special
        }

    def validate_profile_data(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate profile data for background information
        """
        errors = []

        # Validate software experience
        software_experience = profile_data.get('software_experience')
        if software_experience is not None:
            valid_software_levels = ['beginner', 'intermediate', 'advanced']
            if software_experience not in valid_software_levels:
                errors.append(f"Software experience must be one of: {', '.join(valid_software_levels)}")

        # Validate hardware knowledge
        hardware_knowledge = profile_data.get('hardware_knowledge')
        if hardware_knowledge is not None:
            valid_hardware_levels = ['none', 'basic', 'electronics', 'robotics', 'advanced']
            if hardware_knowledge not in valid_hardware_levels:
                errors.append(f"Hardware knowledge must be one of: {', '.join(valid_hardware_levels)}")

        # Validate interests
        interests = profile_data.get('interests')
        if interests is not None:
            if not isinstance(interests, list):
                errors.append("Interests must be a list")
            else:
                if len(interests) > 10:
                    errors.append("Cannot have more than 10 interests")

                valid_interests = {'AI', 'Web', 'Mobile', 'Embedded', 'Data', 'Robotics'}
                for interest in interests:
                    if interest not in valid_interests:
                        errors.append(f"Interest '{interest}' is not valid. Valid interests are: {', '.join(sorted(valid_interests))}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize user input to prevent injection attacks
        """
        # Remove potentially dangerous characters
        sanitized = input_str.strip()

        # Prevent script tags and other dangerous HTML
        dangerous_patterns = [
            r'<script', r'</script>', r'javascript:', r'vbscript:',
            r'on\w+\s*=', r'<iframe', r'</iframe>', r'<object', r'</object>'
        ]

        for pattern in dangerous_patterns:
            import re
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)

        return sanitized

    def validate_user_registration(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate all user registration data
        """
        errors = []

        # Validate email
        email = user_data.get('email', '')
        if not email or not self.validate_email(email):
            errors.append("Invalid email format")

        # Validate username
        username = user_data.get('username', '')
        if not username or not self.validate_username(username):
            errors.append("Invalid username format. Username must be 3-50 characters and contain only letters, numbers, and underscores")

        # Validate password
        password = user_data.get('password', '')
        password_validation = self.validate_password_strength(password)
        if not password_validation['is_valid']:
            errors.extend(password_validation['errors'])

        # Validate profile data
        profile_validation = self.validate_profile_data(user_data)
        if not profile_validation['is_valid']:
            errors.extend(profile_validation['errors'])

        # Check for duplicate emails/username handled by DB constraints
        # but we can do a preliminary check here if needed

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "password_validation": password_validation,
            "profile_validation": profile_validation
        }

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt
        """
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a secure random token
        """
        return secrets.token_urlsafe(length)

    def validate_full_name(self, full_name: str) -> Dict[str, Any]:
        """
        Validate full name format
        """
        errors = []

        if full_name is not None:
            if len(full_name) > 100:
                errors.append("Full name must be at most 100 characters long")
            if full_name.strip() == '':
                errors.append("Full name cannot be empty")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }

    def validate_user_update(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user profile update data
        """
        errors = []

        # Validate email if provided
        email = update_data.get('email')
        if email is not None and not self.validate_email(email):
            errors.append("Invalid email format")

        # Validate full name if provided
        full_name = update_data.get('full_name')
        if full_name is not None:
            name_validation = self.validate_full_name(full_name)
            if not name_validation['is_valid']:
                errors.extend(name_validation['errors'])

        # Validate profile data if provided
        profile_validation = self.validate_profile_data(update_data)
        if not profile_validation['is_valid']:
            errors.extend(profile_validation['errors'])

        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }