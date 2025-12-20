from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from src.database import get_db
from src.models.user import User
from src.services.rag import rag_service
from src.utils.auth import get_current_active_user
from pydantic import BaseModel

router = APIRouter(tags=["ask"])

class AskQuery(BaseModel):
    question: str
    top_k: int = 5

class AskResponse(BaseModel):
    answer: str
    sources: list = []

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    query: AskQuery,
    db: Session = Depends(get_db)
):
    """
    RAG-powered Q&A endpoint
    Ask a question about the textbook content and get an AI-generated answer
    """
    try:
        # Process the RAG query
        result = rag_service.query_with_sources(query.question, query.top_k)

        return AskResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )


@router.post("/ask/advanced")
async def ask_question_advanced(
    query: AskQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Advanced RAG-powered Q&A endpoint with more options
    """
    try:
        # For now, just return the same result with more detailed information
        result = rag_service.query_with_sources(query.question, query.top_k)

        return {
            "question": query.question,
            "answer": result["answer"],
            "sources": result["sources"],
            "total_sources_found": len(result["sources"]),
            "query_config": {
                "top_k": query.top_k
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )