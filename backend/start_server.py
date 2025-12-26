#!/usr/bin/env python3
"""
Start script for the Physical AI & Humanoid Robotics Textbook API
Designed for easy deployment to Hugging Face Spaces or other cloud platforms
"""

import os
import sys
from pathlib import Path

# Add the python_backend directory to the path so imports work correctly
python_backend_path = Path(__file__).parent / "python_backend"
sys.path.insert(0, str(python_backend_path))

# Change to the python_backend directory so relative imports work
original_cwd = os.getcwd()
os.chdir(python_backend_path)

def main():
    """Run the FastAPI application"""
    # Get port from environment variable (required for Hugging Face deployment)
    port = int(os.getenv("PORT", 8000))

    # Import the app after changing the path and directory
    from src.config import settings
    from src.main import app

    print(f"Starting {settings.app_name}...")
    print(f"Debug mode: {settings.debug}")
    print(f"Server will run on port: {port}")
    print("API documentation at: http://localhost:8000/docs")
    print("Admin panel at: http://localhost:8000/redoc")
    print()

    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",  # Bind to all interfaces for external access
        port=port,
        reload=settings.debug,  # Auto-reload in debug mode
        log_level="info" if not settings.debug else "debug",
        # Workers for production (set to 1 for Hugging Face Spaces)
        workers=int(os.getenv("WORKERS", 1))
    )

if __name__ == "__main__":
    try:
        main()
    finally:
        # Restore original working directory
        os.chdir(original_cwd)