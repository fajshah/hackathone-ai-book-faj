from typing import List, Dict, Any
from src.services.embeddings import embeddings_service
from src.config import settings
import openai
import logging
from openai import OpenAI
import os

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Determine which provider to use - prioritize OpenRouter if available
        if settings.openrouter_api_key:
            self.api_key = settings.openrouter_api_key
            self.model = settings.openrouter_model
            self.base_url = "https://openrouter.ai/api/v1"
        else:
            self.api_key = settings.openai_api_key
            self.model = settings.openai_model
            self.base_url = None  # Use default OpenAI base URL

        self.client = None
        # Don't initialize the client here to avoid quota issues during startup

    def query(self, question: str, context_chunks: List[Dict[str, Any]] = None, top_k: int = 5) -> str:
        """
        Process a RAG query by searching for relevant chunks and generating a response

        Args:
            question: The question to answer
            context_chunks: Optional pre-fetched context chunks
            top_k: Number of top similar chunks to retrieve

        Returns:
            Generated answer based on the context and question
        """
        if context_chunks is None:
            # Search for relevant chunks using embeddings
            context_chunks = embeddings_service.search_similar(question, limit=top_k)

        # Format the context from retrieved chunks
        context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])

        # Prepare the prompt for OpenAI
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics textbook.
        Use the following context to answer the question. If the context doesn't contain
        enough information, say so clearly.

        Context:
        {context_text}

        Question: {question}

        Answer:
        """

        try:
            # Initialize client only when needed and if not already initialized
            if self.client is None:
                try:
                    if self.base_url:
                        # Use OpenRouter with custom base URL
                        self.client = OpenAI(
                            api_key=self.api_key,
                            base_url=self.base_url
                        )
                    else:
                        # Use OpenAI with default settings
                        self.client = OpenAI(api_key=self.api_key)
                except Exception as init_error:
                    logger.error(f"Failed to initialize API client: {str(init_error)}")
                    # Return a response based on context without calling API
                    context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                    return f"Based on the provided context: {context_text[:500]}... [Note: API client is not available, showing raw context]"

            # Call API to generate response using the client instance
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. Provide accurate, helpful answers based on the context provided. Be concise but thorough."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            answer = response.choices[0].message.content.strip()
            return answer

        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            # Even if OpenAI fails, try to return context-based response
            if context_chunks:
                context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                return f"Based on the provided context: {context_text[:500]}... [Note: OpenAI API call failed, showing raw context]"
            return "Sorry, I encountered an error while processing your question. Please try again later."

    def query_with_sources(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process a RAG query and return both the answer and source information

        Args:
            question: The question to answer
            top_k: Number of top similar chunks to retrieve

        Returns:
            Dictionary containing the answer and source information
        """
        # Search for relevant chunks
        context_chunks = embeddings_service.search_similar(question, limit=top_k)

        # Generate the answer
        answer = self.query(question, context_chunks, top_k)

        # Return answer with source information
        return {
            "answer": answer,
            "sources": [
                {
                    "chunk_id": chunk["chunk_id"],
                    "content": chunk["content"][:200] + "..." if len(chunk["content"]) > 200 else chunk["content"],  # Truncate for display
                    "score": chunk["score"],
                    "metadata": chunk["metadata"]
                }
                for chunk in context_chunks
            ]
        }

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        """
        Add a document to the RAG system by chunking and indexing it

        Args:
            doc_id: Unique identifier for the document
            content: Full content of the document
            metadata: Additional metadata about the document
        """
        if metadata is None:
            metadata = {}

        # Simple chunking strategy - split by paragraphs
        paragraphs = content.split('\n\n')

        # Filter out empty paragraphs and short paragraphs
        paragraphs = [p.strip() for p in paragraphs if len(p.strip()) > 50]

        # Add each paragraph as a separate chunk
        for i, paragraph in enumerate(paragraphs):
            chunk_id = f"{doc_id}_chunk_{i}"
            chunk_metadata = {
                **metadata,
                "doc_id": doc_id,
                "chunk_index": i,
                "total_chunks": len(paragraphs)
            }

            # Add to embeddings service
            embeddings_service.add_chunk(
                chunk_id=int(chunk_id.replace("_", "").replace("chunk", "").replace("doc", "")),
                content=paragraph,
                metadata=chunk_metadata
            )

    def update_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        """
        Update a document in the RAG system by removing old chunks and adding new ones
        """
        # In a real implementation, you would first delete old chunks associated with this doc_id
        # For now, we'll just add the new content
        self.add_document(doc_id, content, metadata)

# Create a global instance
rag_service = RAGService()