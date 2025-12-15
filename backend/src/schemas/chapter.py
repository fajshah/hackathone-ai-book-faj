from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChapterBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    order_num: int
    module_id: Optional[int] = None


class ChapterCreate(ChapterBase):
    pass


class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    order_num: Optional[int] = None
    module_id: Optional[int] = None


class Chapter(ChapterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True