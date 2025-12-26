# API Endpoints Documentation

## Authentication Endpoints

### POST /api/auth/signup
Register a new user with profile information.

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string (optional)",
  "software_experience": "string (optional)",
  "hardware_knowledge": "string (optional)",
  "interests": "array (optional)"
}
```

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "full_name": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "software_experience": "string",
  "hardware_knowledge": "string",
  "interests": "array",
  "email_verified": "boolean",
  "last_login_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### POST /api/auth/signin
Authenticate user with email and password.

**Request Body (form-data):**
```
username: email
password: password
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "string",
  "refresh_token": "string"
}
```

### GET /api/auth/me
Get current user details.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "full_name": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "software_experience": "string",
  "hardware_knowledge": "string",
  "interests": "array",
  "email_verified": "boolean",
  "last_login_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### PUT /api/auth/profile
Update user profile information.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "full_name": "string (optional)",
  "email": "string (optional)",
  "is_active": "boolean (optional)",
  "software_experience": "string (optional)",
  "hardware_knowledge": "string (optional)",
  "interests": "array (optional)"
}
```

**Response:**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "full_name": "string",
  "is_active": "boolean",
  "is_admin": "boolean",
  "software_experience": "string",
  "hardware_knowledge": "string",
  "interests": "array",
  "email_verified": "boolean",
  "last_login_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### POST /api/auth/refresh
Refresh the access token using refresh token.

**Request Body:**
```json
{
  "token": "refresh_token"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "string"
}
```

### POST /api/auth/signout
Sign out current user (client-side token removal).

**Response:**
```json
{
  "success": true,
  "message": "Successfully signed out"
}
```

## Content Personalization Endpoints

### GET /api/content/personalized
Get personalized content recommendations based on user profile.

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "user_id": "integer",
  "recommendations": {
    "by_experience": "string",
    "by_interests": "array",
    "by_knowledge": "string",
    "recommended_content": "array"
  },
  "message": "string"
}
```

## Authentication System Integration

The authentication system is fully integrated with:

1. **JWT Token Authentication**: Secure access and refresh token system
2. **Password Security**: Bcrypt hashing with configurable rounds
3. **Profile Data Management**: Separate storage for background information
4. **Session Management**: Automatic last login tracking
5. **Content Personalization**: Dynamic recommendations based on user profile
6. **Data Validation**: Comprehensive input validation for profile fields

## Profile Fields Validation

- **Software Experience**: "beginner", "intermediate", "advanced"
- **Hardware Knowledge**: "none", "basic", "electronics", "robotics", "advanced"
- **Interests**: Array of ["AI", "Web", "Mobile", "Embedded", "Data", "Robotics"]

## Security Features

- Password strength validation
- Account lockout after failed login attempts
- Email verification status tracking
- Active/inactive user status
- Token expiration and refresh mechanisms
- SQL injection prevention through ORM
- Input sanitization and validation

## Integration with Frontend

The API endpoints are designed to work seamlessly with the frontend authentication components:

- Signup form sends profile data during registration
- Signin form handles token storage and redirection
- Profile page allows users to update their background information
- Navbar component displays authentication status
- Main page fetches personalized content based on user profile