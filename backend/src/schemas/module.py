from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    module_type: Optional[str] = None
    week_number: Optional[int] = None


class ModuleCreate(ModuleBase):
    pass


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    module_type: Optional[str] = None
    week_number: Optional[int] = None


class Module(ModuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True