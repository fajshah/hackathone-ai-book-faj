"""
Start script for the Physical AI & Humanoid Robotics Textbook API
"""

import uvicorn
from src.config import settings

def main():
    """Run the FastAPI application"""
    print(f"Starting {settings.app_name}...")
    print(f"Debug mode: {settings.debug}")
    print("Access the API at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Admin panel at: http://localhost:8000/redoc")
    print()

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,  # Auto-reload in debug mode
        log_level="info" if not settings.debug else "debug"
    )

if __name__ == "__main__":
    main()