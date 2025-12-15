from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChunkBase(BaseModel):
    content: str
    chunk_type: Optional[str] = "text"
    source_document: Optional[str] = None
    source_page: Optional[int] = None
    chapter_id: Optional[int] = None
    module_id: Optional[int] = None
    metadata_json: Optional[str] = None


class ChunkCreate(ChunkBase):
    pass


class ChunkUpdate(BaseModel):
    content: Optional[str] = None
    chunk_type: Optional[str] = None
    source_document: Optional[str] = None
    source_page: Optional[int] = None
    chapter_id: Optional[int] = None
    module_id: Optional[int] = None
    metadata_json: Optional[str] = None


class Chunk(ChunkBase):
    id: int
    embedding_vector: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True