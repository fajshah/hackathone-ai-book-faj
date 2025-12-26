from typing import List, Dict, Any, Optional
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingsService:
    def __init__(self):
        try:
            # Initialize Qdrant client
            if settings.qdrant_url and settings.qdrant_url.startswith('https://'):
                # Use URL for cloud Qdrant instance
                self.client = QdrantClient(
                    url=settings.qdrant_url,
                    api_key=settings.qdrant_api_key
                )
            else:
                # Use host/port for local Qdrant instance
                # Extract host and port from URL if in format http://host:port
                import re
                if settings.qdrant_url:
                    match = re.match(r'http://([^:]+):(\d+)', settings.qdrant_url)
                    if match:
                        host = match.group(1)
                        port = int(match.group(2))
                        self.client = QdrantClient(
                            host=host,
                            port=port,
                            api_key=settings.qdrant_api_key
                        )
                    else:
                        # Default to localhost if URL format is not recognized
                        self.client = QdrantClient(
                            host="localhost",
                            port=6333,
                            api_key=settings.qdrant_api_key
                        )
                else:
                    # Default to localhost
                    self.client = QdrantClient(
                        host="localhost",
                        port=6333,
                        api_key=settings.qdrant_api_key
                    )
            self.collection_name = settings.qdrant_collection_name
            self.vector_size = 1536  # Default for OpenAI embeddings
            self._ensure_collection_exists()
        except Exception as e:
            logger.error(f"Error initializing Qdrant client: {str(e)}")
            # Create a mock client that returns empty results
            self.client = None
            self.collection_name = settings.qdrant_collection_name
            self.vector_size = 1536

    def _ensure_collection_exists(self):
        """Ensure the collection exists in Qdrant"""
        if self.client is None:
            logger.warning("Qdrant client not available, skipping collection check")
            return

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
        if self.client is None:
            logger.warning("Qdrant client not available, skipping chunk addition")
            return

        if metadata is None:
            metadata = {}

        embedding = self.create_embedding(content)

        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "text": content,  # Use 'text' to match the embedding scripts
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
        if self.client is None:
            logger.warning("Qdrant client not available, skipping chunks addition")
            return

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
        try:
            query_embedding = self.create_embedding(query)

            # Search for similar content in Qdrant database
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )

            return [
                {
                    "chunk_id": result.id,  # Use the point ID as chunk_id
                    "content": result.payload.get("text", ""),  # Use 'text' instead of 'content'
                    "score": result.score,
                    "metadata": {
                        k: v for k, v in result.payload.items()
                        if k not in ["text"]  # Exclude 'text' from metadata, include everything else
                    }
                }
                for result in results
            ]
        except Exception as e:
            logger.error(f"Error in Qdrant search: {str(e)}")
            # Return empty results if Qdrant is not available
            return []

    def update_chunk(self, chunk_id: int, content: str, metadata: Dict[str, Any] = None):
        """Update an existing text chunk in the vector database"""
        if self.client is None:
            logger.warning("Qdrant client not available, skipping chunk update")
            return

        if metadata is None:
            metadata = {}

        embedding = self.create_embedding(content)

        point = PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "text": content,  # Use 'text' to match the embedding scripts
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
        if self.client is None:
            logger.warning("Qdrant client not available, skipping chunk deletion")
            return

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.PointIdsList(
                points=[chunk_id]
            )
        )

        logger.info(f"Deleted chunk {chunk_id} from vector database")

    def delete_chunks_by_metadata(self, metadata_filter: Dict[str, Any]):
        """Delete chunks based on metadata filter"""
        if self.client is None:
            logger.warning("Qdrant client not available, skipping chunks deletion by metadata")
            return

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

# Create a global instance with error handling
try:
    embeddings_service = EmbeddingsService()
except Exception as e:
    logger.error(f"Failed to initialize embeddings service: {str(e)}")
    # Create a mock service that handles requests gracefully
    class MockEmbeddingsService:
        def search_similar(self, query: str, limit: int = 5):
            return []

        def add_chunk(self, chunk_id: int, content: str, metadata=None):
            pass

        def add_chunks(self, chunks_data):
            pass

        def update_chunk(self, chunk_id: int, content: str, metadata=None):
            pass

        def delete_chunk(self, chunk_id: int):
            pass

        def delete_chunks_by_metadata(self, metadata_filter):
            pass

    embeddings_service = MockEmbeddingsService()