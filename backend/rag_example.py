"""
Working RAG example for the Physical AI & Humanoid Robotics textbook
This script demonstrates the RAG functionality with sample data
"""

import asyncio
import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.services.rag import rag_service
from src.services.embeddings import embeddings_service
from src.utils.sample_data import get_sample_chunks
from src.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_rag_example():
    """Run a complete RAG example with sample data"""
    print("=== Physical AI & Humanoid Robotics Textbook RAG Example ===\n")

    # Step 1: Add sample chunks to the vector database
    print("1. Adding sample textbook content to vector database...")

    sample_chunks = get_sample_chunks()

    for i, chunk_data in enumerate(sample_chunks):
        chunk_id = i + 1
        content = chunk_data['content']

        # Add to vector store
        embeddings_service.add_chunk(
            chunk_id=chunk_id,
            content=content,
            metadata={
                "module_id": chunk_data.get("module_id"),
                "chapter_id": chunk_data.get("chapter_id"),
                "source_document": chunk_data.get("source_document")
            }
        )
        print(f"   Added chunk {chunk_id}: {content[:50]}...")

    print(f"\nSuccessfully added {len(sample_chunks)} chunks to the vector database.\n")

    # Step 2: Test RAG queries
    test_questions = [
        "What is Physical AI?",
        "Explain ROS 2 architecture",
        "How does simulation help in robotics development?",
        "What is the NVIDIA Isaac platform?",
        "What are Vision-Language-Action models?"
    ]

    print("2. Running RAG queries...\n")

    for question in test_questions:
        print(f"Question: {question}")
        print("-" * 50)

        # Get response with sources
        result = rag_service.query_with_sources(question, top_k=3)

        print(f"Answer: {result['answer']}")
        print(f"Sources used: {len(result['sources'])}")

        for i, source in enumerate(result['sources'], 1):
            print(f"  Source {i}: {source['content'][:100]}...")

        print("\n" + "="*80 + "\n")

    # Step 3: Test a more complex query
    print("3. Testing a complex multi-topic query...")

    complex_question = "How do ROS 2, simulation environments, and NVIDIA Isaac work together in a robotics project?"
    print(f"Question: {complex_question}")
    print("-" * 50)

    result = rag_service.query_with_sources(complex_question, top_k=5)
    print(f"Answer: {result['answer']}")

    print(f"\nSources used: {len(result['sources'])}")
    for i, source in enumerate(result['sources'], 1):
        print(f"  Source {i}: {source['content'][:150]}...")

    print("\n=== RAG Example Completed Successfully ===")


def main():
    """Main function to run the RAG example"""
    print(f"Using OpenAI model: {settings.openai_model}")
    print(f"Using Qdrant collection: {settings.qdrant_collection_name}")
    print(f"Using embedding dimension: {embeddings_service.vector_size}")
    print()

    # Run the async function
    asyncio.run(run_rag_example())


if __name__ == "__main__":
    main()