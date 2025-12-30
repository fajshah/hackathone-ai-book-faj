# Hugging Face Space Deployment Guide

This guide provides instructions for deploying the Physical AI & Humanoid Robotics Textbook API to Hugging Face Spaces.

## Prerequisites

- Hugging Face account
- Qdrant cloud instance with populated data
- Required API keys and URLs

## Environment Variables Setup

Set the following secrets in your Hugging Face Space:

```env
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=physical_ai
OPENAI_API_KEY=your_openai_api_key  # or use OpenRouter
```

## Repository Structure

For Hugging Face Space deployment, your repository should have this structure:

```
your-space-repo/
├── app.py                 # Entry point for Hugging Face Spaces
├── requirements.txt       # Python dependencies
├── backend/
│   ├── python_backend/
│   │   ├── main.py
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── services/
│   │   ├── routers/
│   │   └── start_server.py
```

## Deployment Steps

### 1. Prepare the Backend

The backend is already configured for Hugging Face deployment:

- Uses `PORT` environment variable
- Handles `WORKERS` configuration
- Proper error handling and logging
- Qdrant connection with retry logic

### 2. Hugging Face Space Configuration

Create a `app.py` file in the root of your repository (already created):

```python
"""
Hugging Face Space App Entry Point
This file serves as the entry point for Hugging Face Spaces deployment
"""
import os
import uvicorn
from backend.python_backend.main import app
from backend.python_backend.config import settings

# This is the app instance that Hugging Face Spaces will look for
print(f"Starting {settings.app_name} for Hugging Face Spaces...")
print(f"Environment: {settings.node_env}")
print(f"Qdrant Collection: {settings.qdrant_collection_name}")

if __name__ == "__main__":
    # For local testing
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "backend.python_backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug
    )
```

### 3. Requirements File

Your `requirements.txt` should include:

```
fastapi==0.115.0
uvicorn==0.32.0
sqlalchemy==2.0.23
psycopg2-binary
qdrant-client==1.8.0
openai==1.54.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
python-multipart==0.0.17
python-dotenv==1.0.0
alembic==1.13.1
pydantic==2.10.1
pydantic-settings==2.6.1
requests==2.32.3
numpy==1.26.4
langchain==0.3.4
langchain-openai==0.2.4
tiktoken==0.8.0
```

### 4. Space Configuration

Create a `README.md` for your Space:

```markdown
---
title: Physical AI & Humanoid Robotics Textbook API
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8000
pinned: false
---

# Physical AI & Humanoid Robotics Textbook API

This Space provides a Qdrant-powered search and RAG system for the Physical AI & Humanoid Robotics textbook.

## API Endpoints

- `/health` - General health check
- `/health/qdrant` - Qdrant connection health
- `/api/ask/public` - Public Q&A endpoint
- `/docs` - API documentation

## Environment Variables Required

- `QDRANT_URL` - Your Qdrant cloud URL
- `QDRANT_API_KEY` - Your Qdrant API key
- `QDRANT_COLLECTION_NAME` - Collection name (default: physical_ai)
```

### 5. Deployment Process

1. **Create a new Hugging Face Space** or use an existing one
2. **Add the required secrets** in Space settings → Secrets
3. **Push your code** to the Space repository
4. **Wait for the build** to complete
5. **Monitor the logs** for any startup issues

### 6. Health Checks

After deployment, verify these endpoints work:

- `https://your-username-space-name.hf.space/health` → `{"status":"healthy"}`
- `https://your-username-space-name.hf.space/health/qdrant` → `{"connected":true,"collection":"physical_ai","points":{"count":<number>}}`

## Troubleshooting

### Common Issues:

1. **Qdrant Connection Failures**:
   - Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
   - Check that the collection name matches `QDRANT_COLLECTION_NAME`
   - Ensure the Qdrant instance is accessible from Hugging Face servers

2. **Environment Variables Not Loading**:
   - Make sure secrets are added as Space Secrets, not regular environment variables
   - Restart the Space after adding secrets

3. **Build Failures**:
   - Check requirements.txt for compatible versions
   - Ensure all dependencies can be installed in the Hugging Face environment

### Logging

Check Space logs for detailed error information:
- Look for Qdrant connection messages
- Verify collection names and point counts
- Monitor for any API key or connection issues

## API Usage

### Public Q&A Endpoint

```bash
curl -X POST "https://your-username-space-name.hf.space/api/ask/public" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Physical AI?",
    "top_k": 5
  }'
```

Expected response format:
```json
{
  "answer": "Physical AI is...",
  "sources": [...],
  "session_id": "..."
}
```

## Frontend Integration

The backend is designed to work with the Docusaurus frontend. The `/api/ask/public` endpoint is optimized for frontend consumption with proper CORS headers.

The AskTheBook component is environment-aware:
- In development (localhost): Connects to local backend
- In production: Connects to Hugging Face Space backend
- Includes automatic fallback to iframe if API fails

## Performance Considerations

- Qdrant connection uses retry logic for reliability
- Embedding generation is optimized for performance
- API responses include source information for transparency
```
