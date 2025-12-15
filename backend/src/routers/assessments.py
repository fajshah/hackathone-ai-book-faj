from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.assessment import Assessment as AssessmentModel
from src.models.user import User
from src.schemas.assessment import Assessment, AssessmentCreate, AssessmentUpdate
from src.utils.auth import get_current_active_user

router = APIRouter(tags=["assessments"])

@router.get("/assessments", response_model=List[Assessment])
async def get_assessments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all assessments with pagination"""
    assessments = db.query(AssessmentModel).offset(skip).limit(limit).all()
    return assessments


@router.get("/assessments/{assessment_id}", response_model=Assessment)
async def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific assessment by ID"""
    assessment = db.query(AssessmentModel).filter(AssessmentModel.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    return assessment


@router.post("/assessments", response_model=Assessment)
async def create_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new assessment"""
    db_assessment = AssessmentModel(**assessment.model_dump())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.put("/assessments/{assessment_id}", response_model=Assessment)
async def update_assessment(
    assessment_id: int,
    assessment_update: AssessmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific assessment"""
    db_assessment = db.query(AssessmentModel).filter(AssessmentModel.id == assessment_id).first()
    if not db_assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    # Update fields
    update_data = assessment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assessment, field, value)

    db.commit()
    db.refresh(db_assessment)
    return db_assessment


@router.delete("/assessments/{assessment_id}")
async def delete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific assessment"""
    assessment = db.query(AssessmentModel).filter(AssessmentModel.id == assessment_id).first()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    db.delete(assessment)
    db.commit()
    return {"message": "Assessment deleted successfully"}