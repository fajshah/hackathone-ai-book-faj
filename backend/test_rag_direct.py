#!/usr/bin/env python3
"""
Script to test the RAG functionality directly
"""
import asyncio
from backend.src.services.embeddings import EmbeddingsService
from backend.src.services.rag import RAGService

# Initialize the services
embeddings_service = EmbeddingsService()
rag_service = RAGService()

# Test a simple search query
query = "What is Physical AI?"

print("Testing RAG functionality...")
print(f"Query: {query}")

try:
    # Test the embeddings search directly
    print("\n1. Testing embeddings search...")
    search_results = embeddings_service.search_similar(query, limit=3)
    print(f"Found {len(search_results)} results:")

    for i, result in enumerate(search_results):
        print(f"  Result {i+1}:")
        print(f"    chunk_id: {result.get('chunk_id')}")
        print(f"    score: {result.get('score')}")
        print(f"    content preview: {result.get('content', '')[:100]}...")
        print(f"    metadata: {result.get('metadata')}")
        print()

    # Test the full RAG query
    print("2. Testing full RAG query...")
    answer = rag_service.query(query, context_chunks=search_results, top_k=3)
    print(f"Answer: {answer}")

    # Test the RAG query with sources
    print("\n3. Testing RAG query with sources...")
    result_with_sources = rag_service.query_with_sources(query, top_k=3)
    print(f"Answer: {result_with_sources['answer']}")
    print(f"Sources: {len(result_with_sources['sources'])} sources")

except Exception as e:
    print(f"Error during testing: {str(e)}")
    import traceback
    traceback.print_exc()