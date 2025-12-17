"""
Hugging Face Space App for Physical AI & Humanoid Robotics Textbook API

This file provides compatibility for Hugging Face Spaces deployment.
The API can be accessed through the Space's endpoint.
"""

import os
import uvicorn
from src.main import app

# For Hugging Face Spaces, the port is set by the environment
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    # Start the FastAPI application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False  # Disable reload for production
    )