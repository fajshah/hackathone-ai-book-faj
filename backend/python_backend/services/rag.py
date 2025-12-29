from typing import List, Dict, Any
from services.embeddings import embeddings_service
from config import settings
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

    def query(self, question: str, context_chunks: List[Dict[str, Any]] = None, top_k: int = 5, conversation_context: List[Dict[str, str]] = None) -> str:
        """
        Process a RAG query by searching for relevant chunks and generating a response

        Args:
            question: The question to answer
            context_chunks: Optional pre-fetched context chunks
            top_k: Number of top similar chunks to retrieve
            conversation_context: Previous conversation messages for context

        Returns:
            Generated answer based on the context and question
        """
        if context_chunks is None:
            # Search for relevant chunks using embeddings
            context_chunks = embeddings_service.search_similar(question, limit=top_k)

        # Format the context from retrieved chunks
        context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])

        # Build conversation history for context if provided
        conversation_history = ""
        if conversation_context:
            conversation_history = "\n\nPrevious conversation:\n"
            for msg in conversation_context[-5:]:  # Use last 5 messages to avoid token limits
                role = msg.get("role", "user")
                content = msg.get("content", "")
                conversation_history += f"{role.capitalize()}: {content}\n"

        # Prepare the prompt for OpenAI - provide context and question separately
        prompt = f"""
        {conversation_history}

        Context:
        {context_text}

        Question: {question}

        Provide a clear, concise answer based on the context above. Do not include the context chunks in your response, only provide the synthesized answer to the question.
        """

        try:
            # Initialize client only when needed and if not already initialized
            if self.client is None:
                try:
                    if self.base_url:
                        # Use OpenRouter with custom base URL
                        # Create client without passing proxies parameter to avoid compatibility issues
                        import os
                        # Temporarily clear proxy environment variables that might cause issues
                        original_http_proxy = os.environ.get('HTTP_PROXY')
                        original_https_proxy = os.environ.get('HTTPS_PROXY')

                        # Remove proxy settings that might cause the 'proxies' parameter issue
                        os.environ.pop('HTTP_PROXY', None)
                        os.environ.pop('HTTPS_PROXY', None)

                        try:
                            self.client = OpenAI(
                                api_key=self.api_key,
                                base_url=self.base_url
                            )
                        finally:
                            # Restore original proxy settings
                            if original_http_proxy:
                                os.environ['HTTP_PROXY'] = original_http_proxy
                            if original_https_proxy:
                                os.environ['HTTPS_PROXY'] = original_https_proxy
                    else:
                        # Use OpenAI with default settings
                        self.client = OpenAI(api_key=self.api_key)
                except TypeError as te:
                    if 'proxies' in str(te):
                        # Handle the specific proxies parameter compatibility issue
                        logger.error(f"Proxy-related error initializing API client: {str(te)}")
                        # Create client with http_client parameter to avoid proxy issues
                        import httpx
                        # Create a client without proxy configuration
                        http_client = httpx.Client()
                        if self.base_url:
                            self.client = OpenAI(
                                api_key=self.api_key,
                                base_url=self.base_url,
                                http_client=http_client
                            )
                        else:
                            self.client = OpenAI(
                                api_key=self.api_key,
                                http_client=http_client
                            )
                    else:
                        logger.error(f"Type error initializing API client: {str(te)}")
                        raise
                except Exception as init_error:
                    logger.error(f"Failed to initialize API client: {str(init_error)}")
                    # Return a response based on context without calling API
                    context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                    return f"Based on the provided context: {context_text[:500]}... [Note: API client is not available, showing raw context]"

            # Call API to generate response using the client instance
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": """You are an AI assistant for the Physical AI & Humanoid Robotics textbook. You MUST generate a final natural-language answer using ONLY the provided retrieved context.

STRICT RULES (DO NOT BREAK):

1. Use ONLY the given context. Do not use outside knowledge.
2. Do NOT mention similarity scores, embeddings, retrieval, or chunks.
3. Do NOT list chapters unless it improves clarity.
4. Do NOT copy long passages verbatim.
5. Do NOT hallucinate or infer beyond the context.
6. Do NOT return the context chunks themselves - only return the synthesized answer.
7. Do NOT include phrases like "Based on the provided context" or "According to the context".

ANSWER STYLE:

- Clear, academic, and student-friendly
- Explain concepts as written in the book
- Prefer concise explanations over verbosity
- Reference chapter/section only when helpful

CONTEXT HANDLING:

- Use ONLY the most relevant context
- Ignore weak or irrelevant sections
- If multiple relevant sections exist, synthesize them logically

FAILSAFE BEHAVIOR:

- If the question cannot be answered from the context, respond with EXACTLY this sentence and nothing else:

  "This information is not available in the provided text."

PURPOSE:

Your role is to help students understand the textbook content.
You are NOT a general-purpose AI assistant."""},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            answer = response.choices[0].message.content.strip()
            return answer

        except openai.AuthenticationError:
            logger.error("OpenAI authentication failed - invalid API key")
            # Even if OpenAI fails, try to return context-based response
            if context_chunks:
                context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                return f"Based on the provided context: {context_text[:500]}... [Note: API authentication failed, showing raw context]"
            return "Sorry, there's an issue with the API configuration. Please contact the administrator."
        except openai.RateLimitError:
            logger.error("OpenAI rate limit exceeded")
            if context_chunks:
                context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                return f"Based on the provided context: {context_text[:500]}... [Note: Rate limit reached, showing raw context]"
            return "We've reached our API usage limit. Please try again later."
        except openai.APIConnectionError:
            logger.error("Failed to connect to OpenAI API")
            if context_chunks:
                context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                return f"Based on the provided context: {context_text[:500]}... [Note: Connection failed, showing raw context]"
            return "Unable to connect to the AI service. Please check your connection and try again."
        except Exception as e:
            logger.error(f"Error in RAG query: {str(e)}")
            # Even if OpenAI fails, try to return context-based response
            if context_chunks:
                context_text = "\n\n".join([chunk["content"] for chunk in context_chunks if chunk["content"]])
                return f"Based on the provided context: {context_text[:500]}... [Note: Processing error occurred, showing raw context]"
            return "Sorry, I encountered an error while processing your question. Please try again later."

    def query_with_sources(self, question: str, top_k: int = 5, conversation_context: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Process a RAG query and return both the answer and source information

        Args:
            question: The question to answer
            top_k: Number of top similar chunks to retrieve
            conversation_context: Previous conversation messages for context

        Returns:
            Dictionary containing the answer and source information
        """
        # Search for relevant chunks
        context_chunks = embeddings_service.search_similar(question, limit=top_k)

        # Generate the answer with conversation context
        answer = self.query(question, context_chunks, top_k, conversation_context)

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