# Physical AI Textbook System - Hugging Face Space Deployment Setup

This document provides a complete setup guide for deploying the Physical AI & Humanoid Robotics Textbook system to Hugging Face Space.

## 📋 Complete System Overview

### Backend Components
- **FastAPI Server**: Main application with health checks and API endpoints
- **Qdrant Integration**: Vector database for textbook content search
- **RAG System**: Retrieval-Augmented Generation for textbook Q&A
- **Environment Management**: Proper handling of secrets and configuration

### Frontend Components
- **AskTheBook Component**: React component with API + iframe fallback
- **Docusaurus Integration**: Seamless embedding in documentation site
- **Responsive Design**: Mobile-friendly with inline CSS isolation

## 🚀 Step-by-Step Deployment Process

### Step 1: Prepare Hugging Face Space Repository

1. Create a new Hugging Face Space or prepare existing repository
2. Structure your repository as follows:
```
your-space-repo/
├── app.py                 # Entry point for Hugging Face Spaces
├── requirements.txt       # Python dependencies
├── backend/
│   └── python_backend/
│       ├── main.py        # FastAPI application
│       ├── config.py      # Configuration settings
│       ├── services/      # Embeddings and RAG services
│       ├── routers/       # API route definitions
│       └── start_server.py # Server startup script
```

### Step 2: Set Up Environment Variables (Secrets)

In your Hugging Face Space settings, add the following secrets:

```
QDRANT_URL = your_qdrant_cloud_url
QDRANT_API_KEY = your_qdrant_api_key
QDRANT_COLLECTION_NAME = physical_ai
OPENAI_API_KEY = your_openai_api_key
```

### Step 3: Verify Backend Files

Ensure these files are present in your repository:

**app.py** (in root directory):
```python
"""
Hugging Face Space App Entry Point
"""
import os
import uvicorn
from backend.python_backend.main import app
from backend.python_backend.config import settings

print(f"Starting {settings.app_name} for Hugging Face Spaces...")
print(f"Environment: {settings.node_env}")
print(f"Qdrant Collection: {settings.qdrant_collection_name}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "backend.python_backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug
    )
```

**requirements.txt**:
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

### Step 4: Frontend Integration

The frontend component is already configured:
- Located at `/frontend/AskTheBook.tsx`
- Integrated in Docusaurus at `/src/pages/ask-the-book.tsx`
- Uses API endpoint: `https://your-space-name.hf.space/api/ask/public`
- Has fallback to iframe if API fails

## 🔧 API Endpoints Reference

### Health Checks
- `GET /health` → `{"status": "healthy"}`
- `GET /health/qdrant` → `{"connected": true, "collection": "physical_ai", "points": {"count": <number>}}`

### Main API
- `POST /api/ask/public` → Textbook Q&A endpoint
  - Request: `{"question": "your question", "top_k": 5}`
  - Response: `{"answer": "...", "sources": [...], "session_id": "..."}`

## 🧪 Testing After Deployment

After your Hugging Face Space is running, verify these endpoints:

```bash
# Health check
curl https://your-username-space-name.hf.space/health

# Qdrant health
curl https://your-username-space-name.hf.space/health/qdrant

# API functionality
curl -X POST https://your-username-space-name.hf.space/api/ask/public \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?", "top_k": 3}'
```

## 🛠️ Troubleshooting

### Common Issues:

1. **Qdrant Connection Issues**:
   - Verify `QDRANT_URL` and `QDRANT_API_KEY` are correct
   - Check that the collection `physical_ai` exists in your Qdrant instance
   - Ensure Qdrant is accessible from Hugging Face servers

2. **Environment Variables Not Loading**:
   - Make sure secrets are added as Space Secrets (not regular environment variables)
   - Restart the Space after adding new secrets

3. **API Rate Limits**:
   - Check OpenAI or OpenRouter usage limits
   - Consider implementing caching for frequently asked questions

4. **CORS Issues**:
   - The backend already allows necessary origins in config.py
   - Check if your frontend domain is in the allowed_origins list

## 🎯 Expected Behavior

After deployment, your system will:
- ✅ Provide textbook-based answers via API
- ✅ Show health status for backend and Qdrant
- ✅ Handle errors gracefully with fallback mechanisms
- ✅ Maintain Docusaurus theme integrity
- ✅ Work identically to localhost behavior
- ✅ Support both API and iframe fallback modes

## 📊 API Response Format

The `/api/ask/public` endpoint returns:
```json
{
  "answer": "Detailed answer from textbook content...",
  "sources": [
    {
      "chunk_id": 1,
      "content": "Relevant text chunk...",
      "score": 0.85,
      "metadata": {"chapter": "Chapter 1", "section": "Section 1.1"}
    }
  ],
  "session_id": "unique-session-identifier"
}
```

## 🔄 Maintenance

- Monitor Space logs for any connection or performance issues
- Keep dependencies up-to-date in requirements.txt
- Regularly verify Qdrant connection and collection integrity
- Test API functionality periodically to ensure textbook content remains accessible