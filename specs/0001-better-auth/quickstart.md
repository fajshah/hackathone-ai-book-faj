# Quickstart Guide: Better Auth Integration

## Prerequisites
- Python 3.8+ with pip
- Node.js 16+ with npm (for frontend components)
- Database (SQLite/PostgreSQL) with SQLAlchemy
- Environment variables configured

## Installation

### Backend Setup
1. Install Better Auth Python package:
```bash
pip install better-auth
```

2. Add authentication dependencies to requirements.txt:
```
better-auth==1.0.0
python-multipart==0.0.6
passlib[bcrypt]==1.7.4
```

### Frontend Setup
1. Install Better Auth frontend components:
```bash
npm install better-auth
```

## Configuration

### Environment Variables
```bash
# Authentication
AUTH_SECRET=your-super-secret-key-here
AUTH_BASE_PATH=/api/auth

# Database
DATABASE_URL=sqlite:///./book_app.db

# Email (SMTP)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## Database Migration

Update your database models to include profile fields:

```python
# backend/src/database.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    email_verified = Column(Boolean, default=False)
    software_experience = Column(String)  # "beginner", "intermediate", "advanced"
    hardware_knowledge = Column(String)   # "none", "basic", "electronics", "robotics", "advanced"
    interests = Column(String)  # JSON string: '["AI", "Robotics"]'
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
```

## API Endpoints Implementation

### 1. Setup Better Auth in main application

```python
# backend/main.py
from fastapi import FastAPI
from better_auth import auth

app = FastAPI()

# Initialize Better Auth
auth = auth(
    secret="your-secret-key",
    database_url="sqlite:///./book_app.db",
    base_path="/api/auth"
)

# Include auth routes
app.include_router(auth.router)
```

### 2. Create custom profile endpoints

```python
# backend/src/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from better_auth import auth
from backend.src.database import get_db
from backend.src.models import User
import json

router = APIRouter()

@router.put("/profile")
async def update_profile(
    profile_data: dict,
    current_user = Depends(auth.current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update profile fields
    if "software_experience" in profile_data:
        user.software_experience = profile_data["software_experience"]
    if "hardware_knowledge" in profile_data:
        user.hardware_knowledge = profile_data["hardware_knowledge"]
    if "interests" in profile_data:
        user.interests = json.dumps(profile_data["interests"])

    db.commit()
    return {"success": True, "profile": {
        "software_experience": user.software_experience,
        "hardware_knowledge": user.hardware_knowledge,
        "interests": json.loads(user.interests) if user.interests else []
    }}
```

## Frontend Implementation

### 1. Create Signup Form with Profile Fields

```jsx
// frontend/components/SignupForm.jsx
import { useState } from 'react';
import { useAuth } from 'better-auth/react';

export default function SignupForm() {
  const { signUp } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    software_experience: 'beginner',
    hardware_knowledge: 'none',
    interests: []
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await signUp.email(formData);
    } catch (error) {
      console.error('Signup error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({...formData, email: e.target.value})}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={formData.password}
        onChange={(e) => setFormData({...formData, password: e.target.value})}
        required
      />
      <select
        value={formData.software_experience}
        onChange={(e) => setFormData({...formData, software_experience: e.target.value})}
      >
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
      </select>
      <select
        value={formData.hardware_knowledge}
        onChange={(e) => setFormData({...formData, hardware_knowledge: e.target.value})}
      >
        <option value="none">None</option>
        <option value="basic">Basic</option>
        <option value="electronics">Electronics</option>
        <option value="robotics">Robotics</option>
        <option value="advanced">Advanced</option>
      </select>
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

### 2. Create Profile Management Component

```jsx
// frontend/components/ProfileManager.jsx
import { useState, useEffect } from 'react';
import { useAuth } from 'better-auth/react';

export default function ProfileManager() {
  const { user, signIn, signOut } = useAuth();
  const [profile, setProfile] = useState({
    software_experience: '',
    hardware_knowledge: '',
    interests: []
  });

  useEffect(() => {
    if (user) {
      setProfile({
        software_experience: user.software_experience || 'beginner',
        hardware_knowledge: user.hardware_knowledge || 'none',
        interests: user.interests || []
      });
    }
  }, [user]);

  const updateProfile = async () => {
    try {
      const response = await fetch('/api/auth/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${user.token}`
        },
        body: JSON.stringify(profile)
      });
      if (response.ok) {
        alert('Profile updated successfully');
      }
    } catch (error) {
      console.error('Profile update error:', error);
    }
  };

  return (
    <div>
      <h2>Profile Management</h2>
      <div>
        <label>Software Experience:</label>
        <select
          value={profile.software_experience}
          onChange={(e) => setProfile({...profile, software_experience: e.target.value})}
        >
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>
      <div>
        <label>Hardware Knowledge:</label>
        <select
          value={profile.hardware_knowledge}
          onChange={(e) => setProfile({...profile, hardware_knowledge: e.target.value})}
        >
          <option value="none">None</option>
          <option value="basic">Basic</option>
          <option value="electronics">Electronics</option>
          <option value="robotics">Robotics</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>
      <button onClick={updateProfile}>Update Profile</button>
    </div>
  );
}
```

## Testing

### Unit Tests
```bash
# Run backend tests
python -m pytest backend/tests/test_auth.py

# Run frontend tests
npm test
```

### Manual Testing Steps
1. Start the backend server
2. Navigate to signup page
3. Fill in credentials and profile information
4. Verify account creation and profile data storage
5. Test signin with created account
6. Verify profile information is accessible
7. Test profile update functionality

## Deployment

1. Set environment variables in production
2. Run database migrations
3. Build frontend assets
4. Deploy to production environment
5. Verify authentication flows work correctly