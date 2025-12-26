from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from database import engine, Base
from routers import chapters, modules, chunks, assessments, ask, auth, admin, content
from config import settings
from middleware.security import setup_security

# Create tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="Physical AI & Humanoid Robotics Textbook API",
    version="1.0.0"
)

# Setup security features
setup_security(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, prefix="/api", tags=["authentication"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(chapters.router, prefix="/api", tags=["chapters"])
app.include_router(modules.router, prefix="/api", tags=["modules"])
app.include_router(chunks.router, prefix="/api", tags=["chunks"])
app.include_router(assessments.router, prefix="/api", tags=["assessments"])
app.include_router(ask.router, prefix="/api", tags=["ask"])
app.include_router(content.router, prefix="/api", tags=["content"])

@app.get("/")
async def root():
    return {"message": "Physical AI & Humanoid Robotics Textbook API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/health/qdrant")
async def qdrant_health_check():
    from services.embeddings import embeddings_service
    try:
        # Test Qdrant connection by counting points
        count = embeddings_service.client.count(collection_name=embeddings_service.collection_name)
        return {
            "status": "healthy",
            "connection": True,
            "collection_exists": True,
            "points_count": count.count,
            "collection_name": embeddings_service.collection_name
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "connection": False,
            "error": str(e),
            "collection_name": embeddings_service.collection_name if hasattr(embeddings_service, 'collection_name') else "unknown"
        }