from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # The actual text chunk
    embedding_vector = Column(String, nullable=True)  # Store as JSON string for now
    chunk_type = Column(String, default="text")  # e.g., "text", "code", "image_desc"
    source_document = Column(String, nullable=True)  # Source document identifier
    source_page = Column(Integer, nullable=True)  # Page number in source
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=True)
    metadata_json = Column(Text, nullable=True)  # Additional metadata as JSON
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())