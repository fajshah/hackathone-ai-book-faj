from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    assessment_type: Optional[str] = "quiz"
    difficulty_level: Optional[str] = "beginner"
    time_limit_minutes: Optional[int] = None
    max_attempts: Optional[int] = 1
    is_active: Optional[bool] = True
    chapter_id: Optional[int] = None
    module_id: Optional[int] = None


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    assessment_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    time_limit_minutes: Optional[int] = None
    max_attempts: Optional[int] = None
    is_active: Optional[bool] = None
    chapter_id: Optional[int] = None
    module_id: Optional[int] = None


class Assessment(AssessmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True