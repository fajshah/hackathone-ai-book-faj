# Physical AI & Humanoid Robotics Textbook API

This is a FastAPI-based backend for the Physical AI & Humanoid Robotics textbook application, featuring RAG (Retrieval Augmented Generation) capabilities with Qdrant vector store and OpenAI integration.

## Features

- **Qdrant Vector Store**: For efficient similarity search of textbook content
- **OpenAI Integration**: For generating intelligent responses to questions
- **PostgreSQL Database**: Powered by Neon for storing structured data
- **RAG System**: Combines textbook content with AI to answer questions
- **Authentication**: User management and security features
- **Admin Panel**: For content management and system monitoring

## Environment Variables

The application requires the following environment variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://your-neon-db-url
NEON_DATABASE_URL=postgresql://your-neon-db-url

# Qdrant Configuration
QDRANT_URL=https://your-qdrant-cluster-url
QDRANT_API_KEY=your-qdrant-api-key

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Server Configuration
PORT=8000
```

## Deployment

This application is designed for easy deployment to Hugging Face Spaces or other cloud platforms:

1. Set the required environment variables
2. Run the application using: `python start_server.py`

## API Endpoints

- `/` - Root endpoint
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
- `/health` - Health check endpoint
- `/api/ask` - RAG-based question answering
- `/api/auth/*` - Authentication endpoints
- `/api/admin/*` - Administrative endpoints

## Architecture

The backend uses:
- **FastAPI** for the web framework
- **SQLAlchemy** for database ORM with PostgreSQL
- **Qdrant** for vector similarity search
- **OpenAI API** for generating responses
- **Pydantic** for data validation