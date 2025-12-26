# Authentication Implementation Documentation

## Overview
This document details the implementation of the authentication system with user profile collection and content personalization for the Physical AI & Humanoid Robotics Book Assistant application.

## Features Implemented

### 1. User Authentication System
- **Signup Flow**: Collects user background information during registration
- **Signin Flow**: Secure login with JWT token management
- **Profile Management**: Update user background information
- **Session Management**: Token-based authentication with refresh tokens

### 2. User Profile Collection
During signup, the system collects:
- **Software Experience**: Beginner, Intermediate, Advanced
- **Hardware Knowledge**: None, Basic, Electronics, Robotics, Advanced
- **Interests**: AI, Web, Mobile, Embedded, Data, Robotics

### 3. Database Schema Extensions
Extended the User model with:
- `software_experience`: VARCHAR field for experience level
- `hardware_knowledge`: VARCHAR field for knowledge level
- `interests`: JSON field for storing user interests
- `email_verified`: BOOLEAN field for email verification status
- `last_login_at`: TIMESTAMP field for tracking last login

### 4. Content Personalization
- Dynamic content recommendations based on user profile
- Learning path suggestions tailored to experience level
- Interest-based content delivery

## File Changes Summary

### Backend Changes

#### `backend/src/models/user.py`
- Extended User model with profile fields
- Added proper column definitions and constraints
- Implemented JSON serialization for interests field

#### `backend/src/schemas/user.py`
- Updated user schemas to include profile fields
- Added comprehensive validation for all fields
- Implemented field validators for data integrity

#### `backend/src/routers/auth.py`
- Implemented comprehensive authentication API endpoints
- Added signup, signin, profile management endpoints
- Created content personalization endpoints
- Implemented proper serialization/deserialization

#### `backend/src/services/auth.py`
- Created authentication service with business logic
- Implemented user registration, authentication, profile updates
- Added content recommendation logic

#### `backend/src/config/auth.py`
- Created authentication configuration module
- Added password hashing utilities
- Implemented token creation functions

#### `backend/alembic/versions/301e930ec861_add_profile_fields_to_user_table.py`
- Database migration for profile fields
- Added all new columns to existing users table

#### `backend/src/main.py`
- Added content router to main application
- Integrated content endpoints

#### `backend/src/services/validation_service.py`
- Created comprehensive validation service
- Added input sanitization and password strength validation

#### `backend/src/services/content_personalization.py`
- Created content personalization service
- Implemented experience-based and interest-based content delivery

### Frontend Changes

#### `frontend/lib/auth.js`
- Created Better Auth client implementation
- Added signup, signin, signout methods
- Implemented profile update and content personalization methods
- Fixed SSR compatibility issues

#### `frontend/contexts/AuthContext.js`
- Created React Context for authentication state management
- Implemented user state, loading states, and error handling

#### `frontend/pages/auth/signup.js`
- Updated signup form with background questions
- Integrated with AuthContext
- Added proper validation and error handling

#### `frontend/pages/auth/signin.js`
- Updated signin form with proper authentication flow
- Integrated with AuthContext

#### `frontend/pages/auth/profile.js`
- Created profile management page
- Added ability to update background information

#### `frontend/components/Navbar.js`
- Updated navigation to use AuthContext
- Added dynamic display of login/logout buttons

#### `frontend/components/Layout.js`
- Created consistent layout component
- Wrapped content with common styling

#### `frontend/pages/index.js`
- Updated main page to use AuthContext
- Added personalized content display based on user profile

#### `frontend/.env.local`
- Added NEXT_PUBLIC_API_URL configuration
- Points to backend API at http://localhost:8001

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/signup` - User registration with profile data
- `POST /api/auth/signin` - User login
- `PUT /api/auth/profile` - Update user profile
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/signout` - User logout

### Content Endpoints
- `GET /api/content/personalized` - Get personalized content based on user profile
- `GET /api/content/recommendations` - Get content recommendations

## Security Features

### Input Validation
- Comprehensive validation for all user inputs
- Password strength requirements
- Email format validation
- Profile field validation

### Authentication Security
- JWT token-based authentication
- Secure password hashing (bcrypt)
- Token refresh mechanism
- Proper session management

### Data Protection
- Input sanitization to prevent injection attacks
- Proper error handling without information disclosure
- Secure storage of sensitive data

## Content Personalization Logic

### Experience-Based Content
- Beginner: Basic concepts, introductory materials
- Intermediate: Core concepts, practical applications
- Advanced: Advanced topics, research papers, complex implementations

### Interest-Based Recommendations
- AI-focused content for AI-interested users
- Hardware-focused content for robotics/electronics interested users
- Software-focused content for web/mobile/embedded interested users

### Learning Path Generation
- Sequential learning paths based on experience level
- Cross-domain recommendations for broader knowledge
- Adaptive content based on user progress

## Frontend Integration

### React Context API
- Centralized authentication state management
- Loading and error state handling
- Automatic token management

### UI Components
- Responsive and user-friendly authentication forms
- Profile management interface
- Personalized content display sections
- Navigation based on authentication status

### UI Adaptation from Docusaurus
The frontend UI was originally designed for Docusaurus documentation site and has been adapted to include:
- Authentication forms (signup/signin) integrated with existing layout
- Profile management pages that match the existing design language
- Navigation elements that fit with the original Docusaurus-inspired styling
- Content personalization sections that blend with the existing UI
- Consistent styling using Tailwind CSS classes that match the original design

## Port Configuration
- Backend: http://localhost:8001
- Frontend: Automatically finds available port (3000-3006 in testing)
- Environment configuration for API connection

## Error Handling

### Frontend Error Handling
- Graceful error messages for users
- Automatic token refresh on expiration
- Proper session cleanup on errors

### Backend Error Handling
- Comprehensive error responses
- Proper HTTP status codes
- Secure error message formatting

## Testing Considerations

### Authentication Flow Testing
- Signup with various profile combinations
- Signin with valid/invalid credentials
- Profile update functionality
- Content personalization accuracy

### Security Testing
- Input validation testing
- Authentication bypass attempts
- Token security verification
- Session management testing

## Deployment Notes

### Environment Variables Required
- `NEXT_PUBLIC_API_URL`: Frontend API base URL
- Backend environment variables for database, secrets, etc.

### Production Considerations
- SSL/TLS for secure communication
- Proper CORS configuration
- Production database setup
- Token expiration policies