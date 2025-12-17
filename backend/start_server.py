#!/usr/bin/env python3
"""
Start script for the Physical AI & Humanoid Robotics Textbook API
Designed for easy deployment to Hugging Face Spaces or other cloud platforms
"""

import os
import uvicorn
from src.config import settings

def main():
    """Run the FastAPI application"""
    # Get port from environment variable (required for Hugging Face deployment)
    port = int(os.getenv("PORT", 8000))

    print(f"Starting {settings.app_name}...")
    print(f"Debug mode: {settings.debug}")
    print(f"Server will run on port: {port}")
    print("API documentation at: http://localhost:8000/docs")
    print("Admin panel at: http://localhost:8000/redoc")
    print()

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",  # Bind to all interfaces for external access
        port=port,
        reload=settings.debug,  # Auto-reload in debug mode
        log_level="info" if not settings.debug else "debug",
        # Workers for production (set to 1 for Hugging Face Spaces)
        workers=int(os.getenv("WORKERS", 1))
    )

if __name__ == "__main__":
    main()