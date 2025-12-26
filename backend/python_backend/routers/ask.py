from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import logging
from database import get_db
from models.user import User
from services.rag import rag_service
from utils.auth import get_current_active_user
from utils.session_manager import session_manager
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(tags=["ask"])

class ConversationMessage(BaseModel):
    role: str
    content: str

class AskQuery(BaseModel):
    question: str
    top_k: int = 5
    conversation_context: list[ConversationMessage] = []
    session_id: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    sources: list = []
    session_id: Optional[str] = None

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    query: AskQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    RAG-powered Q&A endpoint with personalization
    Ask a question about the textbook content and get an AI-generated answer
    """
    try:
        # Handle session management
        session_id = query.session_id
        if not session_id:
            session_id = session_manager.create_session()

        # Get conversation history from session if not provided in request
        if not query.conversation_context:
            session_history = session_manager.get_conversation_history(session_id, limit=5)
            conversation_context = session_history
        else:
            conversation_context = [msg.dict() for msg in query.conversation_context]

        # Process the RAG query with conversation context
        result = rag_service.query_with_sources(query.question, query.top_k, conversation_context)

        # Personalize the answer based on user profile
        personalized_answer = personalize_answer(result["answer"], current_user)

        # Add user question and AI response to session history
        session_manager.add_message_to_session(session_id, "user", query.question)
        session_manager.add_message_to_session(session_id, "assistant", result["answer"])

        return AskResponse(
            answer=personalized_answer,
            sources=result["sources"],
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Error in /ask endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry, there was an error processing your question. Please try again later."
        )


@router.post("/ask/public", response_model=AskResponse)
async def ask_question_public(
    query: AskQuery,
    db: Session = Depends(get_db)
):
    """
    Public RAG-powered Q&A endpoint without authentication
    Ask a question about the textbook content and get an AI-generated answer
    Personalization will use default values for unauthenticated users
    """
    try:
        # Handle session management
        session_id = query.session_id
        if not session_id:
            session_id = session_manager.create_session()

        # Get conversation history from session if not provided in request
        if not query.conversation_context:
            session_history = session_manager.get_conversation_history(session_id, limit=5)
            conversation_context = session_history
        else:
            conversation_context = [msg.dict() for msg in query.conversation_context]

        # Process the RAG query with conversation context
        result = rag_service.query_with_sources(query.question, query.top_k, conversation_context)

        # Create a mock user with default values for personalization
        from unittest.mock import Mock
        mock_user = Mock()
        mock_user.software_experience = "beginner"
        mock_user.hardware_knowledge = "none"
        mock_user.interests = ["AI", "Robotics"]

        # Personalize the answer based on default profile
        personalized_answer = personalize_answer(result["answer"], mock_user)

        # Add user question and AI response to session history
        session_manager.add_message_to_session(session_id, "user", query.question)
        session_manager.add_message_to_session(session_id, "assistant", result["answer"])

        return AskResponse(
            answer=personalized_answer,
            sources=result["sources"],
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Error in /ask/public endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry, there was an error processing your question. Please try again later."
        )


def personalize_answer(answer: str, user: User) -> str:
    """
    Personalize the answer based on user's profile
    """
    import re

    # Get user profile information
    experience_level = user.software_experience or "beginner"
    hardware_knowledge = user.hardware_knowledge or "none"
    interests = user.interests or []

    # Personalize based on experience level
    if experience_level == "beginner":
        # Add more explanations and basic concepts for beginners
        answer = add_beginner_explanations(answer)
    elif experience_level == "intermediate":
        # Add some advanced concepts while keeping it accessible
        answer = add_intermediate_context(answer)
    elif experience_level == "advanced":
        # Include more technical depth and research context
        answer = add_advanced_context(answer)

    # Add hardware-specific context if relevant
    if hardware_knowledge in ["electronics", "robotics", "advanced"]:
        answer = add_hardware_context(answer)

    # Add interest-specific context
    if "AI" in interests:
        answer = add_ai_context(answer)
    if "Robotics" in interests:
        answer = add_robotics_context(answer)
    if "Data" in interests:
        answer = add_data_context(answer)

    return answer


def add_beginner_explanations(answer: str) -> str:
    """
    Add beginner-friendly explanations to the answer
    """
    # Add basic definitions and simpler explanations
    beginner_additions = [
        "\n\n**For beginners:** This concept might seem complex at first, but think of it as...",
        "\n\n**Key takeaway for beginners:** Focus on understanding the fundamental principle first before moving to advanced applications.",
        "\n\n**Beginner tip:** Try implementing a simple version of this concept to build intuition."
    ]

    # Add beginner-friendly additions to the answer
    import random
    if random.random() > 0.5:  # Add with 50% probability
        answer += beginner_additions[0]

    return answer


def add_intermediate_context(answer: str) -> str:
    """
    Add intermediate-level context to the answer
    """
    # Add more detailed explanations and connections
    intermediate_additions = [
        "\n\n**Implementation note:** For practical applications, consider...",
        "\n\n**Advanced consideration:** More sophisticated approaches might involve...",
        "\n\n**Practical tip:** When implementing this, pay attention to..."
    ]

    import random
    if random.random() > 0.5:  # Add with 50% probability
        answer += intermediate_additions[0]

    return answer


def add_advanced_context(answer: str) -> str:
    """
    Add advanced-level context to the answer
    """
    # Add research context, advanced techniques, and cutting-edge approaches
    advanced_additions = [
        "\n\n**Research perspective:** Current research in this area focuses on...",
        "\n\n**Advanced implementation:** State-of-the-art approaches use...",
        "\n\n**Cutting-edge note:** Recent papers have explored..."
    ]

    import random
    if random.random() > 0.5:  # Add with 50% probability
        answer += advanced_additions[0]

    return answer


def add_hardware_context(answer: str) -> str:
    """
    Add hardware-specific context to the answer
    """
    if any(keyword in answer.lower() for keyword in ["algorithm", "model", "system", "process"]):
        hardware_additions = [
            "\n\n**Hardware consideration:** This algorithm's performance can be significantly improved with specialized hardware like GPUs or TPUs.",
            "\n\n**Implementation note:** Consider the hardware constraints when deploying this system.",
            "\n\n**Hardware tip:** For real-time applications, optimize for your target hardware architecture."
        ]

        import random
        if random.random() > 0.7:  # Add with 30% probability
            answer += hardware_additions[0]

    return answer


def add_ai_context(answer: str) -> str:
    """
    Add AI-specific context to the answer
    """
    if any(keyword in answer.lower() for keyword in ["algorithm", "model", "learning", "data", "system"]):
        ai_additions = [
            "\n\n**AI perspective:** This approach is commonly used in machine learning applications.",
            "\n\n**ML connection:** This concept is fundamental to understanding modern AI systems.",
            "\n\n**AI application:** This technique has shown great success in various AI domains."
        ]

        import random
        if random.random() > 0.7:  # Add with 30% probability
            answer += ai_additions[0]

    return answer


def add_robotics_context(answer: str) -> str:
    """
    Add robotics-specific context to the answer
    """
    if any(keyword in answer.lower() for keyword in ["system", "control", "sensor", "algorithm", "model"]):
        robotics_additions = [
            "\n\n**Robotics application:** This concept is crucial for autonomous robot systems.",
            "\n\n**Robotic implementation:** In robotics, this would typically involve real-time processing.",
            "\n\n**Robotics perspective:** This approach is commonly used in robotic control systems."
        ]

        import random
        if random.random() > 0.7:  # Add with 30% probability
            answer += robotics_additions[0]

    return answer


def add_data_context(answer: str) -> str:
    """
    Add data-specific context to the answer
    """
    if any(keyword in answer.lower() for keyword in ["model", "algorithm", "system", "process", "analysis"]):
        data_additions = [
            "\n\n**Data science note:** This method is particularly effective with large datasets.",
            "\n\n**Data perspective:** Consider the data quality and preprocessing requirements.",
            "\n\n**Statistical consideration:** The effectiveness depends on the underlying data distribution."
        ]

        import random
        if random.random() > 0.7:  # Add with 30% probability
            answer += data_additions[0]

    return answer


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