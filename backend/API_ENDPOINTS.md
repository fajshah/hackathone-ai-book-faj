# API Endpoints Documentation

## Backend Authentication API Endpoints
The following authentication endpoints are available from the backend server running at http://localhost:8001:

### Authentication Endpoints
- `POST /api/auth/signup` - User registration with profile data
- `POST /api/auth/signin` - User login
- `PUT /api/auth/profile` - Update user profile
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/signout` - User logout

### Content Endpoints
- `GET /api/content/personalized` - Get personalized content based on user profile
- `GET /api/content/recommendations` - Get content recommendations

## Usage from Frontend
To use these endpoints from the frontend, make fetch requests to the backend:

```javascript
// Example signup request
const response = await fetch('http://localhost:8001/api/auth/signup', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword123',
    full_name: 'John Doe',
    username: 'johndoe',
    software_experience: 'intermediate',
    hardware_knowledge: 'electronics',
    interests: ['AI', 'Robotics']
  })
});
```

## Current Frontend State
The frontend currently maintains the original UI design without any authentication components, preserving the clean RAG chatbot interface.