from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
from database import get_db
from models.user import User
from models.module import Module
from models.chapter import Chapter
from models.chunk import Chunk
from models.assessment import Assessment
from services.embeddings import embeddings_service
from utils.auth import get_current_admin_user
from config import settings

router = APIRouter(tags=["admin"])

@router.post("/admin/seed")
async def seed_database(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Seed the database with initial textbook content
    This includes modules, chapters, chunks, and assessments
    """
    try:
        # Sample modules for Physical AI & Humanoid Robotics textbook
        modules_data = [
            {
                "title": "Introduction to Physical AI",
                "description": "Foundations of Physical AI and its applications in robotics",
                "content": "Physical AI combines artificial intelligence with physical systems to create intelligent robots that can interact with the real world...",
                "module_type": "Physical AI",
                "week_number": 1
            },
            {
                "title": "ROS 2 Fundamentals",
                "description": "Robot Operating System 2 for robotics development",
                "content": "ROS 2 is the next generation of the Robot Operating System, designed for production environments...",
                "module_type": "ROS 2",
                "week_number": 2
            },
            {
                "title": "Gazebo & Unity Simulation",
                "description": "Simulation environments for robotics development",
                "content": "Gazebo and Unity provide powerful simulation environments for testing and developing robotics applications...",
                "module_type": "Simulation",
                "week_number": 3
            },
            {
                "title": "NVIDIA Isaac Platform",
                "description": "NVIDIA's platform for AI-powered robotics",
                "content": "The NVIDIA Isaac platform provides tools and frameworks for developing AI-powered robots...",
                "module_type": "NVIDIA Isaac",
                "week_number": 4
            },
            {
                "title": "Vision-Language-Action Models",
                "description": "VLA models for embodied AI",
                "content": "Vision-Language-Action models enable robots to understand and interact with the world using vision, language, and action...",
                "module_type": "VLA",
                "week_number": 5
            }
        ]

        # Add modules to database
        for module_data in modules_data:
            existing_module = db.query(Module).filter(Module.title == module_data["title"]).first()
            if not existing_module:
                module = Module(**module_data)
                db.add(module)
        db.commit()

        # Sample chapters
        chapters_data = [
            {
                "title": "What is Physical AI?",
                "description": "Understanding the core concepts of Physical AI",
                "content": "Physical AI is a field that combines artificial intelligence with physical systems to create robots that can perceive, reason, and act in the real world...",
                "order_num": 1,
                "module_id": 1
            },
            {
                "title": "ROS 2 Architecture",
                "description": "Understanding the architecture of ROS 2",
                "content": "ROS 2 uses a client library implementation that provides the middleware for communication between nodes...",
                "order_num": 1,
                "module_id": 2
            },
            {
                "title": "Simulation Environments",
                "description": "Using Gazebo and Unity for robotics simulation",
                "content": "Simulation is crucial for robotics development as it allows testing without physical hardware...",
                "order_num": 1,
                "module_id": 3
            }
        ]

        # Add chapters to database
        for chapter_data in chapters_data:
            existing_chapter = db.query(Chapter).filter(
                Chapter.title == chapter_data["title"],
                Chapter.module_id == chapter_data["module_id"]
            ).first()
            if not existing_chapter:
                chapter = Chapter(**chapter_data)
                db.add(chapter)
        db.commit()

        # Sample chunks for RAG
        chunks_data = [
            {
                "content": "Physical AI combines artificial intelligence with physical systems to create intelligent robots that can interact with the real world. This field encompasses robotics, computer vision, natural language processing, and control theory.",
                "chunk_type": "text",
                "source_document": "introduction_to_physical_ai.md",
                "source_page": 1,
                "module_id": 1,
                "metadata_json": json.dumps({"difficulty": "beginner", "keywords": ["physical ai", "robotics", "artificial intelligence"]})
            },
            {
                "content": "ROS 2 (Robot Operating System 2) is the next generation of the Robot Operating System, designed for production environments. It provides libraries and tools to help software developers create robot applications with features like hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.",
                "chunk_type": "text",
                "source_document": "ros2_fundamentals.md",
                "source_page": 1,
                "module_id": 2,
                "metadata_json": json.dumps({"difficulty": "beginner", "keywords": ["ros2", "robot operating system", "middleware"]})
            },
            {
                "content": "Gazebo is a robot simulator that provides realistic physics simulation and rendering of environments. Unity is a game engine that can be used for robotics simulation with its robotics toolkit. Both platforms allow developers to test algorithms and behaviors in a safe, virtual environment before deploying to real robots.",
                "chunk_type": "text",
                "source_document": "simulation_environments.md",
                "source_page": 1,
                "module_id": 3,
                "metadata_json": json.dumps({"difficulty": "intermediate", "keywords": ["gazebo", "unity", "simulation", "physics"]})
            }
        ]

        # Add chunks to database and vector store
        for i, chunk_data in enumerate(chunks_data):
            # Add to database
            existing_chunk = db.query(Chunk).filter(Chunk.content == chunk_data["content"]).first()
            if not existing_chunk:
                chunk = Chunk(**chunk_data)
                db.add(chunk)
                db.commit()
                db.refresh(chunk)  # Get the ID after commit

                # Add to vector store
                embeddings_service.add_chunk(
                    chunk_id=chunk.id,
                    content=chunk.content,
                    metadata=json.loads(chunk.metadata_json) if chunk.metadata_json else {}
                )

        # Sample assessments
        assessments_data = [
            {
                "title": "Physical AI Quiz 1",
                "description": "Basic concepts of Physical AI",
                "content": "1. What is Physical AI?\n2. Name three components of Physical AI.\n3. How does Physical AI differ from traditional AI?",
                "assessment_type": "quiz",
                "difficulty_level": "beginner",
                "max_attempts": 3,
                "is_active": True,
                "module_id": 1
            },
            {
                "title": "ROS 2 Quiz 1",
                "description": "ROS 2 architecture and concepts",
                "content": "1. What is the main difference between ROS 1 and ROS 2?\n2. Explain the DDS middleware in ROS 2.\n3. How do you create a publisher and subscriber in ROS 2?",
                "assessment_type": "quiz",
                "difficulty_level": "intermediate",
                "max_attempts": 2,
                "is_active": True,
                "module_id": 2
            }
        ]

        # Add assessments to database
        for assessment_data in assessments_data:
            existing_assessment = db.query(Assessment).filter(Assessment.title == assessment_data["title"]).first()
            if not existing_assessment:
                assessment = Assessment(**assessment_data)
                db.add(assessment)
        db.commit()

        return {
            "message": "Database seeded successfully",
            "modules_added": len(modules_data),
            "chapters_added": len(chapters_data),
            "chunks_added": len(chunks_data),
            "assessments_added": len(assessments_data)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error seeding database: {str(e)}"
        )


@router.post("/admin/export")
async def export_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Export all textbook data as JSON"""
    try:
        # Export modules
        modules = db.query(Module).all()
        modules_json = [module.__dict__ for module in modules]
        for module in modules_json:
            module.pop('_sa_instance_state', None)

        # Export chapters
        chapters = db.query(Chapter).all()
        chapters_json = [chapter.__dict__ for chapter in chapters]
        for chapter in chapters_json:
            chapter.pop('_sa_instance_state', None)

        # Export chunks
        chunks = db.query(Chunk).all()
        chunks_json = [chunk.__dict__ for chunk in chunks]
        for chunk in chunks_json:
            chunk.pop('_sa_instance_state', None)

        # Export assessments
        assessments = db.query(Assessment).all()
        assessments_json = [assessment.__dict__ for assessment in assessments]
        for assessment in assessments_json:
            assessment.pop('_sa_instance_state', None)

        return {
            "modules": modules_json,
            "chapters": chapters_json,
            "chunks": chunks_json,
            "assessments": assessments_json
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting data: {str(e)}"
        )


@router.post("/admin/import")
async def import_data(
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Import textbook data from JSON"""
    try:
        # Import modules
        modules_data = data.get("modules", [])
        for module_data in modules_data:
            module_data.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
            existing_module = db.query(Module).filter(Module.title == module_data["title"]).first()
            if not existing_module:
                module = Module(**module_data)
                db.add(module)
        db.commit()

        # Import chapters
        chapters_data = data.get("chapters", [])
        for chapter_data in chapters_data:
            chapter_data.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
            existing_chapter = db.query(Chapter).filter(
                Chapter.title == chapter_data["title"],
                Chapter.module_id == chapter_data["module_id"]
            ).first()
            if not existing_chapter:
                chapter = Chapter(**chapter_data)
                db.add(chapter)
        db.commit()

        # Import chunks
        chunks_data = data.get("chunks", [])
        for chunk_data in chunks_data:
            chunk_data.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
            existing_chunk = db.query(Chunk).filter(Chunk.content == chunk_data["content"]).first()
            if not existing_chunk:
                chunk = Chunk(**chunk_data)
                db.add(chunk)
                db.commit()
                db.refresh(chunk)  # Get the ID after commit

                # Add to vector store
                embeddings_service.add_chunk(
                    chunk_id=chunk.id,
                    content=chunk.content,
                    metadata=json.loads(chunk.metadata_json) if chunk.metadata_json else {}
                )

        # Import assessments
        assessments_data = data.get("assessments", [])
        for assessment_data in assessments_data:
            assessment_data.pop('_sa_instance_state', None)  # Remove SQLAlchemy state
            existing_assessment = db.query(Assessment).filter(Assessment.title == assessment_data["title"]).first()
            if not existing_assessment:
                assessment = Assessment(**assessment_data)
                db.add(assessment)
        db.commit()

        return {
            "message": "Data imported successfully",
            "modules_imported": len(modules_data),
            "chapters_imported": len(chapters_data),
            "chunks_imported": len(chunks_data),
            "assessments_imported": len(assessments_data)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing data: {str(e)}"
        )


@router.get("/admin/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get statistics about the textbook content"""
    try:
        stats = {
            "total_modules": db.query(Module).count(),
            "total_chapters": db.query(Chapter).count(),
            "total_chunks": db.query(Chunk).count(),
            "total_assessments": db.query(Assessment).count(),
            "total_users": db.query(User).count()
        }

        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting stats: {str(e)}"
        )