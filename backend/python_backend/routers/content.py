"""
Content router for personalized content delivery based on user profile
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database import get_db
from models.user import User
from utils.auth import get_current_active_user
from schemas.user import User as UserSchema
from services.content_personalization import ContentPersonalizationService


router = APIRouter(prefix="/api/content", tags=["Content"])


@router.get("/personalized")
def get_personalized_content(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized content recommendations based on user profile
    """
    # Create personalization service instance
    personalization_service = ContentPersonalizationService()

    # Get personalized content based on user profile
    personalized_data = personalization_service.get_personalized_content(current_user)

    return {
        "user_id": current_user.id,
        "personalized_content": personalized_data
    }


@router.get("/learning-path")
def get_learning_path(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized learning path based on user profile
    """
    personalization_service = ContentPersonalizationService()
    personalized_data = personalization_service.get_personalized_content(current_user)

    return {
        "user_id": current_user.id,
        "learning_path": personalized_data["learning_path"],
        "next_steps": personalized_data["recommended_next_steps"]
    }


@router.get("/by-level/{level}")
def get_content_by_level(
    level: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get content appropriate for a specific experience level
    """
    if level not in ["beginner", "intermediate", "advanced"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid level. Must be beginner, intermediate, or advanced")

    personalization_service = ContentPersonalizationService()

    # Temporarily modify user's experience level to get content for that level
    original_experience = current_user.software_experience
    current_user.software_experience = level

    personalized_data = personalization_service.get_personalized_content(current_user)

    # Restore original experience level
    current_user.software_experience = original_experience

    return {
        "target_level": level,
        "content": personalized_data["personalized_content"]["by_level"],
        "difficulty_level": level
    }