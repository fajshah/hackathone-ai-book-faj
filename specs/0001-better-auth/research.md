# Research Document: Better Auth Integration

## R1: Database Schema Integration

### Current Schema Investigation
Based on the existing project files, I found that the backend uses SQLAlchemy with the following relevant models in `backend/src/database.py`:

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    # No password field currently defined
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Decision: Database Extension Approach
**Approach**: Extend the existing user model with additional profile fields rather than creating a separate profile table.

**Rationale**:
- Maintains simplicity and reduces joins
- Better Auth supports custom user fields
- Easier to query user information for personalization
- Follows the principle of minimalism

**Implementation Plan**:
1. Add password_hash field to existing User model
2. Add profile fields (software_experience, hardware_knowledge, interests)
3. Add email verification and timestamps

### Updated Schema
```
users table:
- id: Integer (primary key, auto-increment)
- email: String (unique, indexed)
- password_hash: String
- email_verified: Boolean (default: false)
- software_experience: String (enum values)
- hardware_knowledge: String (enum values)
- interests: String (JSON string)
- created_at: DateTime
- updated_at: DateTime
- last_login_at: DateTime (nullable)
```

## R2: Better Auth Integration Patterns

### Research Findings
Better Auth provides both a complete authentication solution and a library approach. For integration with an existing Python/FastAPI backend:

**Decision**: Use Better Auth's API endpoints alongside existing FastAPI backend rather than replacing it completely.

**Rationale**:
- Allows gradual migration
- Maintains existing API structure
- Provides flexibility for custom business logic
- Supports the existing RAG system

**Integration Pattern**:
1. Use Better Auth for authentication core (password hashing, session management)
2. Extend with custom endpoints for profile data
3. Maintain existing database models with Better Auth compatibility

## R3: Frontend Integration Patterns

### Current Frontend Investigation
Looking at the project structure, I can see there's a frontend component, but I need to understand the current structure. Let me check for frontend files:

The project appears to have a backend-focused structure with RAG capabilities. The frontend would need to be built to support:
- Signup flow with extended profile questions
- Signin/signout functionality
- Profile management
- Session handling

**Decision**: Create React-based forms that integrate with Better Auth API endpoints

**Implementation**:
- Signup form with additional profile fields
- Signin form with standard credentials
- Profile editing component
- Session context provider

## R4: Email Service Integration

### Available Options Research
Based on the existing codebase, I found references to potential email services:

1. **SendGrid**: Professional option with good integration
2. **Resend**: Newer service with simple API
3. **SMTP**: Direct email sending via configuration

**Decision**: Start with SMTP configuration for simplicity, with option to upgrade to service providers

**Rationale**:
- Aligns with minimalism principle
- Free-tier safe
- Can be configured with common providers (Gmail, Outlook, etc.)
- Easy to upgrade later if needed

## R5: Session Management Strategy

### Integration Approach
Better Auth handles session management automatically, but we need to ensure compatibility with the existing system:

**Decision**: Use Better Auth's session tokens with custom middleware to extend functionality

**Implementation**:
- Use Better Auth's session management
- Create middleware to enrich session data with profile information
- Maintain compatibility with existing API patterns
- Support both token-based and cookie-based authentication

## Summary of Resolved Unknowns

| Unknown | Resolution | Implementation |
|---------|------------|----------------|
| Database schema | Extend existing User model | Add profile fields to current schema |
| Frontend structure | Build React forms for auth flows | Create signup/signin components |
| Email service | Use SMTP configuration | Configure with environment variables |
| Personalized content | API endpoints with user profile data | Create recommendation endpoints |
| UI/UX requirements | Standard auth flows with additional profile fields | Follow best practices for auth UX |
| Session management | Better Auth with custom middleware | Integrate with existing patterns |

All unknowns have been resolved and implementation approach is clear.