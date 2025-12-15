from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.chunk import Chunk as ChunkModel
from src.models.user import User
from src.schemas.chunk import Chunk, ChunkCreate, ChunkUpdate
from src.utils.auth import get_current_active_user

router = APIRouter(tags=["chunks"])

@router.get("/chunks", response_model=List[Chunk])
async def get_chunks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all chunks with pagination"""
    chunks = db.query(ChunkModel).offset(skip).limit(limit).all()
    return chunks


@router.get("/chunks/{chunk_id}", response_model=Chunk)
async def get_chunk(
    chunk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific chunk by ID"""
    chunk = db.query(ChunkModel).filter(ChunkModel.id == chunk_id).first()
    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found"
        )
    return chunk


@router.post("/chunks", response_model=Chunk)
async def create_chunk(
    chunk: ChunkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new chunk"""
    db_chunk = ChunkModel(**chunk.model_dump())
    db.add(db_chunk)
    db.commit()
    db.refresh(db_chunk)
    return db_chunk


@router.put("/chunks/{chunk_id}", response_model=Chunk)
async def update_chunk(
    chunk_id: int,
    chunk_update: ChunkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific chunk"""
    db_chunk = db.query(ChunkModel).filter(ChunkModel.id == chunk_id).first()
    if not db_chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found"
        )

    # Update fields
    update_data = chunk_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_chunk, field, value)

    db.commit()
    db.refresh(db_chunk)
    return db_chunk


@router.delete("/chunks/{chunk_id}")
async def delete_chunk(
    chunk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific chunk"""
    chunk = db.query(ChunkModel).filter(ChunkModel.id == chunk_id).first()
    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found"
        )

    db.delete(chunk)
    db.commit()
    return {"message": "Chunk deleted successfully"}