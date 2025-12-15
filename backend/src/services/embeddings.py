from typing import List, Dict, Any, Optional
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from src.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingsService:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key
        )
        self.collection_name = settings.qdrant_collection_name
        self.vector_size = 1536  # Default for OpenAI embeddings
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection exists in Qdrant"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection if it doesn't exist
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection '{self.collection_name}'")

    def create_embedding(self, text: str) -> List[float]:
        """Create an embedding for the given text using a mock OpenAI approach"""
        # In a real implementation, this would call OpenAI's embedding API
        # For now, we'll create a mock embedding using a simple hash-based approach
        # In production, use: openai.Embedding.create(input=text, model="text-embedding-ada-002")

        # Mock embedding generation - in real implementation use OpenAI API
        import hashlib
        import struct

        # Create a deterministic "embedding" based on the text content
        hash_input = text.encode('utf-8')
        embedding = []

        for i in range(self.vector_size):
            # Create a hash based on the text and position
            hash_obj = hashlib.md5(hash_input + str(i).encode('utf-8'))
            hash_hex = hash_obj.hexdigest()
            # Convert hex to a float between -1 and 1
            hash_int = int(hash_hex[:8], 16)  # Take first 8 hex chars
            float_val = (hash_int % 2000000000) / 1000000000.0 - 1.0  # Normalize to [-1, 1]
            embedding.append(float_val)

        return embedding

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts"""
        return [self.create_embedding(text) for text in texts]

    def add_chunk(self, chunk_id: int, content: str, metadata: Dict[str, Any] = None):
        """Add a text chunk to the vector database"""
        if metadata is None:
            metadata = {}

        embedding = self.create_embedding(content)

        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "content": content,
                "chunk_id": chunk_id,
                **metadata
            }
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        logger.info(f"Added chunk {chunk_id} to vector database")

    def add_chunks(self, chunks_data: List[Dict[str, Any]]):
        """Add multiple text chunks to the vector database"""
        points = []

        for chunk_data in chunks_data:
            chunk_id = chunk_data['chunk_id']
            content = chunk_data['content']
            metadata = chunk_data.get('metadata', {})

            embedding = self.create_embedding(content)

            point = PointStruct(
                id=chunk_id,
                vector=embedding,
                payload={
                    "content": content,
                    "chunk_id": chunk_id,
                    **metadata
                }
            )
            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        logger.info(f"Added {len(points)} chunks to vector database")

    def search_similar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar text chunks to the query"""
        query_embedding = self.create_embedding(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=limit
        )

        return [
            {
                "chunk_id": result.payload.get("chunk_id"),
                "content": result.payload.get("content"),
                "score": result.score,
                "metadata": {k: v for k, v in result.payload.items()
                           if k not in ["chunk_id", "content"]}
            }
            for result in results
        ]

    def update_chunk(self, chunk_id: int, content: str, metadata: Dict[str, Any] = None):
        """Update an existing text chunk in the vector database"""
        if metadata is None:
            metadata = {}

        embedding = self.create_embedding(content)

        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "content": content,
                "chunk_id": chunk_id,
                **metadata
            }
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

        logger.info(f"Updated chunk {chunk_id} in vector database")

    def delete_chunk(self, chunk_id: int):
        """Delete a text chunk from the vector database"""
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[chunk_id]
            )
        )

        logger.info(f"Deleted chunk {chunk_id} from vector database")

    def delete_chunks_by_metadata(self, metadata_filter: Dict[str, Any]):
        """Delete chunks based on metadata filter"""
        # Create filter conditions
        conditions = []
        for key, value in metadata_filter.items():
            conditions.append(
                models.FieldCondition(
                    key=f"metadata.{key}",
                    match=models.MatchValue(value=value)
                )
            )

        if conditions:
            filter_condition = models.Filter(must=conditions)

            # Find points to delete first
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_filter=filter_condition,
                limit=10000  # Limit for safety
            )

            point_ids = [result.id for result in search_results]

            if point_ids:
                self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=models.PointIdsList(points=point_ids)
                )

                logger.info(f"Deleted {len(point_ids)} chunks by metadata filter")

# Create a global instance
embeddings_service = EmbeddingsService()