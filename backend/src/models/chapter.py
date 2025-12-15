from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Full chapter content
    order_num = Column(Integer, nullable=False)  # Chapter order in the book
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=True)  # Optional module association
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())