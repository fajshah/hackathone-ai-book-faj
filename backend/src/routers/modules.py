from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.module import Module as ModuleModel
from src.models.user import User
from src.schemas.module import Module, ModuleCreate, ModuleUpdate
from src.utils.auth import get_current_active_user

router = APIRouter(tags=["modules"])

@router.get("/modules", response_model=List[Module])
async def get_modules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all modules with pagination"""
    modules = db.query(ModuleModel).offset(skip).limit(limit).all()
    return modules


@router.get("/modules/{module_id}", response_model=Module)
async def get_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific module by ID"""
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    return module


@router.post("/modules", response_model=Module)
async def create_module(
    module: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new module"""
    # Check if module with same title already exists
    existing_module = db.query(ModuleModel).filter(
        ModuleModel.title == module.title
    ).first()
    if existing_module:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Module with this title already exists"
        )

    db_module = ModuleModel(**module.model_dump())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


@router.put("/modules/{module_id}", response_model=Module)
async def update_module(
    module_id: int,
    module_update: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific module"""
    db_module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not db_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )

    # Update fields
    update_data = module_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_module, field, value)

    db.commit()
    db.refresh(db_module)
    return db_module


@router.delete("/modules/{module_id}")
async def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific module"""
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )

    db.delete(module)
    db.commit()
    return {"message": "Module deleted successfully"}