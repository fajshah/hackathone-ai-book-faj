from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from database import get_db
from models.chunk import Chunk as ChunkModel
from models.user import User
from schemas.chunk import Chunk, ChunkCreate, ChunkUpdate
from utils.auth import get_current_active_user
from services.embeddings import embeddings_service

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
    """Create a new chunk and add to Qdrant vector store"""
    db_chunk = ChunkModel(**chunk.model_dump())
    db.add(db_chunk)
    db.commit()
    db.refresh(db_chunk)

    # Add to Qdrant vector store
    try:
        metadata = json.loads(db_chunk.metadata_json) if db_chunk.metadata_json else {}
        embeddings_service.add_chunk(
            chunk_id=db_chunk.id,
            content=db_chunk.content,
            metadata=metadata
        )
    except Exception as e:
        # If adding to Qdrant fails, still return the chunk but log the error
        import logging
        logging.error(f"Failed to add chunk {db_chunk.id} to Qdrant: {str(e)}")

    return db_chunk


@router.put("/chunks/{chunk_id}", response_model=Chunk)
async def update_chunk(
    chunk_id: int,
    chunk_update: ChunkUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a specific chunk and update in Qdrant vector store"""
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

    # Update in Qdrant vector store
    try:
        metadata = json.loads(db_chunk.metadata_json) if db_chunk.metadata_json else {}
        embeddings_service.update_chunk(
            chunk_id=db_chunk.id,
            content=db_chunk.content,
            metadata=metadata
        )
    except Exception as e:
        # If updating in Qdrant fails, still return the chunk but log the error
        import logging
        logging.error(f"Failed to update chunk {db_chunk.id} in Qdrant: {str(e)}")

    return db_chunk


@router.delete("/chunks/{chunk_id}")
async def delete_chunk(
    chunk_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a specific chunk and remove from Qdrant vector store"""
    chunk = db.query(ChunkModel).filter(ChunkModel.id == chunk_id).first()
    if not chunk:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chunk not found"
        )

    db.delete(chunk)
    db.commit()

    # Remove from Qdrant vector store
    try:
        embeddings_service.delete_chunk(chunk_id)
    except Exception as e:
        # If deleting from Qdrant fails, still return success but log the error
        import logging
        logging.error(f"Failed to delete chunk {chunk_id} from Qdrant: {str(e)}")

    return {"message": "Chunk deleted successfully"}