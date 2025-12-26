#!/usr/bin/env python3
"""
Script to check if Qdrant collection exists and has data
"""
from qdrant_client import QdrantClient
import os

# Use the same Qdrant credentials from the .env file
qdrant_url = "https://bef512c4-0759-464d-af6c-4d6e2352566c.us-east4-0.gcp.cloud.qdrant.io"
qdrant_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.jCpXlK2HGZIHrE5j4iXF1cfFAthAmzXH-Kw-SSUhNFI"

# Initialize Qdrant client
client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

print("Checking Qdrant collections...")

# List all collections
collections = client.get_collections()
print(f"Available collections: {collections}")

# Check if 'physical_ai' collection exists
collection_name = "physical_ai"
try:
    collection_info = client.get_collection(collection_name)
    print(f"\nCollection '{collection_name}' exists!")
    print(f"Points count: {collection_info.points_count}")
    print(f"Config: {collection_info.config}")

    # Try to get a few points to verify data
    if collection_info.points_count > 0:
        print("\nSample points from the collection:")
        points = client.scroll(
            collection_name=collection_name,
            limit=3,
            with_payload=True,
            with_vectors=False
        )

        # The scroll function returns (points, next_page), where points is a list of PointStruct
        retrieved_points, next_page = points
        for point in retrieved_points:
            print(f"ID: {point.id}")
            print(f"Payload keys: {list(point.payload.keys())}")
            for key, value in point.payload.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
            print("---")
    else:
        print(f"\nCollection '{collection_name}' exists but is empty.")

except Exception as e:
    print(f"\nCollection '{collection_name}' does not exist: {str(e)}")

# Also check for 'textbook_chunks' collection
collection_name2 = "textbook_chunks"
try:
    collection_info2 = client.get_collection(collection_name2)
    print(f"\nCollection '{collection_name2}' exists!")
    print(f"Points count: {collection_info2.points_count}")
    print(f"Config: {collection_info2.config}")
except Exception as e:
    print(f"\nCollection '{collection_name2}' does not exist: {str(e)}")