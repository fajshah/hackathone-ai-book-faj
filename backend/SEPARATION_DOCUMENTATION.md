# Docusaurus + Separate Auth Application Setup

This project has been configured to separate the Docusaurus documentation site from the authentication functionality.

## Current Structure

### Docusaurus Site (Main Application)
- **Purpose**: Documentation and content delivery
- **Pages**: Only RAG chatbot interface
- **Location**: `frontend/` directory
- **URL**: http://localhost:3010

### Authentication Backend (Separate Service)
- **Purpose**: User authentication and profile management
- **Location**: `backend/` directory
- **URL**: http://localhost:8001
- **API Endpoints**: `/api/auth/*`

## Running the Applications

### 1. Docusaurus Documentation Site
```bash
cd frontend
npm run dev
```
- Runs on: http://localhost:3010

### 2. Authentication Backend
```bash
cd backend
python start_server.py
```
- Runs on: http://localhost:8001

## Authentication API Endpoints

The authentication functionality is available as a separate service:

- `POST http://localhost:8001/api/auth/signup` - User registration
- `POST http://localhost:8001/api/auth/signin` - User login
- `PUT http://localhost:8001/api/auth/profile` - Update profile
- `GET http://localhost:8001/api/auth/me` - Get user info
- `GET http://localhost:8001/api/content/personalized` - Personalized content

## Integration

To integrate authentication with the Docusaurus site in the future:
1. Create a separate auth application
2. Use API calls to the backend service
3. Maintain complete separation of concerns

## Benefits of This Approach

1. **Clean Separation**: Docusaurus remains focused on documentation
2. **No UI Conflicts**: Authentication doesn't interfere with content
3. **Scalability**: Each service can be scaled independently
4. **Maintainability**: Clear boundaries between services
5. **Flexibility**: Can easily swap authentication systems

## Future Development

If you need to create a separate authentication app:
1. Create a new Next.js application for auth
2. Use the backend API endpoints for authentication
3. Keep Docusaurus focused solely on documentation