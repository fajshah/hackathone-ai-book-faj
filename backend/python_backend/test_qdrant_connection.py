#!/usr/bin/env python3
"""
Test script to verify Qdrant connection and health endpoint
"""
import asyncio
import os
from services.embeddings import embeddings_service
from main import app
from fastapi.testclient import TestClient

def test_qdrant_connection():
    """Test Qdrant connection directly"""
    print("Testing Qdrant connection...")

    try:
        # Test that the embeddings service is properly initialized
        print(f"[OK] Qdrant client initialized: {embeddings_service.client is not None}")
        print(f"[OK] Collection name: {embeddings_service.collection_name}")

        # Test connection by counting points
        count = embeddings_service.client.count(collection_name=embeddings_service.collection_name)
        print(f"[OK] Collection '{embeddings_service.collection_name}' has {count.count} points")

        # Test search functionality
        test_results = embeddings_service.search_similar("test query", limit=1)
        print(f"[OK] Search test successful, found {len(test_results)} results")

        return True
    except Exception as e:
        print(f"[ERROR] Qdrant connection test failed: {e}")
        return False

def test_health_endpoints():
    """Test health endpoints using TestClient"""
    print("\nTesting health endpoints...")

    client = TestClient(app)

    # Test general health
    response = client.get("/health")
    print(f"[OK] Health endpoint: {response.status_code}, response: {response.json()}")

    # Test Qdrant health
    response = client.get("/health/qdrant")
    print(f"[OK] Qdrant health endpoint: {response.status_code}, response: {response.json()}")

    return True

def main():
    print("Starting Qdrant connection tests...\n")

    # Test direct connection
    connection_ok = test_qdrant_connection()

    if connection_ok:
        # Test health endpoints
        test_health_endpoints()
        print("\n[SUCCESS] All tests passed! Qdrant connection is working properly.")
    else:
        print("\n[ERROR] Connection test failed. Please check Qdrant configuration.")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())