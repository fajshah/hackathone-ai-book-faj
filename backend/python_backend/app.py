"""
Hugging Face Space App Entry Point
This file serves as the entry point for Hugging Face Spaces deployment
"""
import os
import uvicorn
from main import app
from config import settings

# This is the app instance that Hugging Face Spaces will look for
# When deployed to Hugging Face Spaces, this will be the entry point
print(f"Starting {settings.app_name} for Hugging Face Spaces...")
print(f"Environment: {settings.node_env}")
print(f"Qdrant Collection: {settings.qdrant_collection_name}")

if __name__ == "__main__":
    # For local testing
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug
    )