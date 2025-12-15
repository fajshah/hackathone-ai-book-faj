# Physical AI & Humanoid Robotics Textbook API

A comprehensive FastAPI backend for the Physical AI & Humanoid Robotics textbook, featuring RAG-powered Q&A, user authentication, and content management.

## Features

- **User Management**: Complete authentication system with JWT tokens and PBKDF2 password hashing
- **Content Management**: Full CRUD APIs for chapters, modules, chunks, and assessments
- **RAG-Powered Q&A**: Advanced question-answering system using vector embeddings and OpenAI
- **Admin Utilities**: Database seeding, import/export, and management tools
- **Security**: Rate limiting, input validation, and security headers
- **Vector Storage**: Qdrant integration for efficient similarity search

## API Endpoints

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh
- `GET /api/auth/me` - Get current user

### Content Management
- `GET /api/modules` - Get all modules
- `POST /api/modules` - Create module
- `GET /api/chapters` - Get all chapters
- `POST /api/chapters` - Create chapter
- `GET /api/chunks` - Get all chunks
- `POST /api/chunks` - Create chunk
- `GET /api/assessments` - Get all assessments
- `POST /api/assessments` - Create assessment

### RAG Services
- `POST /api/ask` - Ask questions about textbook content
- `POST /api/ask/advanced` - Advanced RAG query with detailed sources

### Admin Functions
- `POST /api/admin/seed` - Seed database with sample content
- `POST /api/admin/export` - Export all content as JSON
- `POST /api/admin/import` - Import content from JSON
- `GET /api/admin/stats` - Get content statistics

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables** in `.env`:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost/dbname
   NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

   # Qdrant Configuration
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   QDRANT_API_KEY=your-api-key
   QDRANT_COLLECTION_NAME=textbook_chunks

   # Authentication Configuration
   SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7

   # OpenAI Configuration
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-4-turbo-preview

   # Application Configuration
   APP_NAME=Physical AI & Humanoid Robotics Textbook API
   DEBUG=True
   ```

3. **Install and run Qdrant** (for vector storage):
   ```bash
   # Using Docker
   docker run -p 6333:6333 -p 6334:6334 \
     -v ./qdrant_storage:/qdrant/storage:Z \
     qdrant/qdrant
   ```

4. **Run the application**:
   ```bash
   python start_server.py
   ```

## Usage Examples

### 1. User Registration and Login
```bash
# Register a new user
curl -X POST "http://localhost:8000/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student1@example.com",
    "password": "SecurePassword123",
    "full_name": "John Student"
  }'

# Login to get tokens
curl -X POST "http://localhost:8000/api/auth/login" \
  -d "username=student1" \
  -d "password=SecurePassword123"
```

### 2. Ask Questions about Textbook Content
```bash
# Ask a question (requires authentication)
curl -X POST "http://localhost:8000/api/ask" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Physical AI?",
    "top_k": 3
  }'
```

### 3. Seed Database with Sample Content
```bash
# Seed with sample textbook content (requires admin privileges)
curl -X POST "http://localhost:8000/api/admin/seed" \
  -H "Authorization: Bearer ADMIN_ACCESS_TOKEN"
```

## Architecture

### Database Models
- **User**: User accounts with authentication and authorization
- **Module**: Course modules (e.g., ROS 2, Gazebo, NVIDIA Isaac, VLA)
- **Chapter**: Individual chapters within modules
- **Chunk**: Text chunks for RAG system
- **Assessment**: Quizzes and assignments

### Services
- **Embeddings Service**: Manages vector embeddings using Qdrant
- **RAG Service**: Handles question answering with context retrieval
- **Auth Service**: Manages authentication and authorization

### Security Features
- JWT-based authentication with refresh tokens
- Account lockout after 3 failed login attempts
- Rate limiting to prevent abuse
- Input validation and sanitization
- Security headers on all responses

## RAG Implementation

The RAG (Retrieval-Augmented Generation) system works as follows:

1. **Indexing**: Textbook content is split into chunks and stored as vector embeddings in Qdrant
2. **Retrieval**: When a question is asked, similar chunks are retrieved using vector similarity search
3. **Generation**: OpenAI's GPT model generates an answer using the retrieved context

## Project Structure

```
backend/
├── src/
│   ├── config/           # Configuration settings
│   ├── database/         # Database setup and models
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routers/          # API route definitions
│   ├── services/         # Business logic services
│   │   ├── embeddings.py # Vector embeddings service
│   │   └── rag.py       # RAG question answering service
│   ├── utils/           # Utility functions
│   │   ├── auth.py      # Authentication utilities
│   │   ├── validation.py # Input validation
│   │   └── sample_data.py # Sample textbook content
│   ├── middleware/      # Middleware components
│   └── main.py          # Main application entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── start_server.py      # Server startup script
├── rag_example.py       # RAG functionality demonstration
└── README.md           # This file
```

## Running the RAG Example

To run the RAG example with sample data:

```bash
python rag_example.py
```

This will:
1. Add sample textbook content to the vector database
2. Run several example questions through the RAG system
3. Display answers with source information

## Development

### Adding New Modules
1. Update the database models if needed
2. Create new schemas for the data structures
3. Add new API routes in the routers directory
4. Update the main application to include new routes

### Extending RAG Capabilities
- Modify `src/services/rag.py` to enhance question answering
- Update `src/services/embeddings.py` to improve vector storage
- Add new chunking strategies for different content types

## Deployment

For production deployment:

1. Use environment variables for all sensitive configuration
2. Set `DEBUG=False` in production
3. Use a production-grade database (PostgreSQL with Neon)
4. Deploy Qdrant in a production environment
5. Use a WSGI server like Gunicorn instead of uvicorn for production