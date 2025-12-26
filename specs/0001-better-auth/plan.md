# Implementation Plan: Better Auth Integration

## Technical Context

This plan outlines the implementation of Better Auth for user authentication, including signup with background information collection and signin flows. The implementation will integrate with the existing backend system and provide personalized content delivery based on user profile data.

### Current Architecture
- Backend: Python/FastAPI application
- Frontend: React/Next.js application
- Database: SQLite (with potential for PostgreSQL migration)
- Authentication: New Better Auth integration
- Vector Database: Qdrant for RAG functionality

### Unknowns (NEEDS CLARIFICATION)
None - all unknowns resolved in research.md

### Dependencies
- Better Auth library (v1.0+)
- Database access layer (SQLAlchemy or equivalent)
- Email service integration (SendGrid, Resend, or similar)
- Frontend framework components (React/Next.js)
- Session management utilities

### Technology Choices
- Better Auth: Modern authentication library with React/Next.js support and extensible user profiles
- Database: Continue with current database system while extending for user profiles
- Email: Integration with existing email infrastructure

## Constitution Check

### Alignment with Core Principles
- **Simplicity**: Better Auth provides straightforward authentication with minimal setup
- **Accuracy**: Industry-standard authentication practices with security best practices
- **Minimalism**: Using a single, focused authentication library rather than custom solution
- **Free-tier Safe**: Better Auth has free tier available and minimal operational cost
- **RAG Answers ONLY from Book Text**: Authentication doesn't affect content delivery principles

### Potential Violations (if any)
- None identified - the implementation aligns with all core principles

## Research Plan (Phase 0)

### R1: Database Schema Integration
- **Task**: Research current database schema and determine best approach for extending user profiles
- **Output**: Documentation of current schema and proposed extension approach

### R2: Better Auth Integration Patterns
- **Task**: Research best practices for integrating Better Auth with Python/FastAPI backend
- **Output**: Integration patterns and code examples

### R3: Frontend Integration Patterns
- **Task**: Research how to implement signup forms with additional background questions in the current frontend
- **Output**: Frontend integration guide with sample components

### R4: Email Service Integration
- **Task**: Research email service options compatible with Better Auth for verification emails
- **Output**: Recommended email service with integration steps

### R5: Session Management Strategy
- **Task**: Research how Better Auth sessions can integrate with existing system
- **Output**: Session management approach document

## Data Model (Phase 1)

### User Profile Extension
Based on research (R1), extending the existing SQLAlchemy User model:

```
users table (extends existing model):
- id: Integer (primary key, auto-increment)
- email: String (unique, indexed)
- password_hash: String (encrypted)
- email_verified: Boolean (default: false)
- software_experience: String (enum: "beginner", "intermediate", "advanced")
- hardware_knowledge: String (enum: "none", "basic", "electronics", "robotics", "advanced")
- interests: String (JSON string format: '["AI", "Robotics", "Web"]')
- created_at: DateTime
- updated_at: DateTime
- last_login_at: DateTime (nullable)
```

### Session Management
```
sessions (handled by Better Auth):
- session_token: string (unique, indexed)
- user_id: Integer (foreign key to users.id)
- expires_at: timestamp
- created_at: timestamp
- ip_address: string (nullable)
- user_agent: string (nullable)
```

## API Contracts (Phase 1)

### Authentication Endpoints
```
POST /api/auth/signup
Request:
{
  "email": "user@example.com",
  "password": "securePassword123",
  "software_experience": "intermediate",
  "hardware_knowledge": "robotics",
  "interests": ["AI", "Robotics"]
}

Response (Success):
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "email_verified": false
  }
}

Response (Error):
{
  "success": false,
  "error": "Email already exists" | "Invalid email format" | "Password too weak"
}

---

POST /api/auth/signin
Request:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response (Success):
{
  "success": true,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com",
    "email_verified": true
  }
}

Response (Error):
{
  "success": false,
  "error": "Invalid credentials"
}

---

GET /api/auth/me
Authentication: Bearer token required
Response (Success):
{
  "id": "uuid-string",
  "email": "user@example.com",
  "email_verified": true,
  "software_experience": "intermediate",
  "hardware_knowledge": "robotics",
  "interests": ["AI", "Robotics"],
  "created_at": "timestamp"
}

Response (Error - Unauthorized):
{
  "success": false,
  "error": "Authentication required"
}

---

POST /api/auth/signout
Authentication: Bearer token required
Response:
{
  "success": true
}
```

### Profile Management Endpoints
```
PUT /api/auth/profile
Authentication: Bearer token required
Request:
{
  "software_experience": "advanced",
  "hardware_knowledge": "advanced",
  "interests": ["AI", "Robotics", "Embedded"]
}

Response (Success):
{
  "success": true,
  "profile": {
    "software_experience": "advanced",
    "hardware_knowledge": "advanced",
    "interests": ["AI", "Robotics", "Embedded"]
  }
}

Response (Error):
{
  "success": false,
  "error": "Validation failed" | "User not found"
}
```

## Quickstart Guide (Phase 1)

### Setup Steps
1. Install Better Auth package in backend:
   ```bash
   pip install better-auth
   ```

2. Configure Better Auth with database integration:
   ```python
   # Initialize Better Auth with database adapter
   from better_auth import auth
   import os

   auth = auth(
       secret=os.getenv("AUTH_SECRET"),
       database_url=os.getenv("DATABASE_URL"),
       # Additional configuration for user profiles
   )
   ```

3. Create migration for user profile extensions (if needed)

4. Update frontend to use Better Auth components:
   ```bash
   npm install better-auth
   ```

5. Implement signup form with additional fields for background information

6. Test authentication flows with various user backgrounds

### Testing Strategy
- Unit tests for authentication endpoints
- Integration tests for user profile creation
- Session management tests
- Security tests for password hashing and session validation

## Re-evaluation of Constitution Check Post-Design

The implementation plan continues to align with all core principles:
- Simplicity: Using a proven authentication library
- Accuracy: Industry-standard practices
- Minimalism: Focused implementation without over-engineering
- Free-tier Safe: Architecture supports free-tier operation
- RAG Content: Authentication is separate from content delivery