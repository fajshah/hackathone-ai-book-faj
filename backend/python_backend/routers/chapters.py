from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.chapter import Chapter as ChapterModel
from models.user import User
from schemas.chapter import Chapter, ChapterCreate, ChapterUpdate
from utils.auth import get_current_active_user

router = APIRouter(tags=["chapters"])

@router.get("/chapters", response_model=List[Chapter])
async def get_chapters(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all chapters with pagination"""
    chapters = db.query(ChapterModel).offset(skip).limit(limit).all()
    return chapters


@router.get("/chapters/{chapter_id}", response_model=Chapter)
async def get_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific chapter by ID"""
    chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )
    return chapter


@router.post("/chapters", response_model=Chapter)
async def create_chapter(
    chapter: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new chapter"""
    # Check if chapter with same order number already exists for the module
    if chapter.module_id:
        existing_chapter = db.query(ChapterModel).filter(
            ChapterModel.module_id == chapter.module_id,
            ChapterModel.order_num == chapter.order_num
        ).first()
        if existing_chapter:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chapter with this order number already exists in this module"
            )

    db_chapter = ChapterModel(**chapter.model_dump())
    db.add(db_chapter)
    db.commit()
    db.refresh(db_chapter)
    return db_chapter


@router.put("/chapters/{chapter_id}", response_model=Chapter)
async def update_chapter(
    chapter_id: int,
    chapter_update: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific chapter"""
    db_chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
    if not db_chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    # Update fields
    update_data = chapter_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_chapter, field, value)

    db.commit()
    db.refresh(db_chapter)
    return db_chapter


@router.delete("/chapters/{chapter_id}")
async def delete_chapter(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific chapter"""
    chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chapter not found"
        )

    db.delete(chapter)
    db.commit()
    return {"message": "Chapter deleted successfully"}