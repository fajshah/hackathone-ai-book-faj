from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=False)  # Assessment questions/content
    assessment_type = Column(String, default="quiz")  # e.g., "quiz", "exam", "lab", "assignment"
    difficulty_level = Column(String, default="beginner")  # "beginner", "intermediate", "advanced"
    time_limit_minutes = Column(Integer, nullable=True)  # Time limit for timed assessments
    max_attempts = Column(Integer, default=1)  # Number of allowed attempts
    is_active = Column(Boolean, default=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())