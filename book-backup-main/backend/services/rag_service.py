import json

import httpx
from core.config import get_settings
from qdrant_client import QdrantClient

settings = get_settings()


class RAGService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        self.collection_name = "docusaurus_book"  # Match the ingestion script
        # We'll determine the actual vector size dynamically when needed
        self._vector_size = None  # Will be determined dynamically

    @property
    def vector_size(self):
        """Dynamically determine the vector size from the collection"""
        if self._vector_size is None:
            try:
                collection_info = self.client.get_collection(self.collection_name)
                # Extract vector size from collection config - different versions of Qdrant client may have different attribute names
                if hasattr(collection_info.config, "params"):
                    params = collection_info.config.params
                    # Check for different possible attribute names
                    if hasattr(params, "vectors_config"):
                        self._vector_size = params.vectors_config.size
                    elif hasattr(params, "vector_size"):  # Alternative attribute name
                        self._vector_size = params.vector_size
                    elif hasattr(params, "size"):  # Another possible attribute
                        self._vector_size = params.size
                    else:
                        # Try to access as dictionary if it's a mapping type
                        try:
                            if hasattr(params, '__getitem__'):
                                if 'vectors_config' in params and hasattr(params['vectors_config'], 'size'):
                                    self._vector_size = params['vectors_config'].size
                                elif 'vector_size' in params:
                                    self._vector_size = params['vector_size']
                                else:
                                    # Default fallback
                                    self._vector_size = 1536  # Size for text-embedding-3-small
                            else:
                                # Default fallback
                                self._vector_size = 1536  # Size for text-embedding-3-small
                        except (TypeError, AttributeError):
                            # Default fallback
                            self._vector_size = 1536  # Size for text-embedding-3-small
                else:
                    # Default fallback
                    self._vector_size = 1536  # Size for text-embedding-3-small
            except:
                # If collection doesn't exist yet, use default based on model name
                if "text-embedding-3-large" in settings.EMBEDDING_MODEL:
                    self._vector_size = 3072
                elif "text-embedding-3-small" in settings.EMBEDDING_MODEL:
                    self._vector_size = 1536
                elif "text-embedding-ada" in settings.EMBEDDING_MODEL:
                    self._vector_size = 1536
                elif "qwen3-embedding-8b" in settings.EMBEDDING_MODEL:
                    self._vector_size = 4096  # Qwen3-embedding-8b produces 4096-dim vectors
                elif "qwen" in settings.EMBEDDING_MODEL.lower():
                    self._vector_size = 1024  # Default for other Qwen models
                else:
                    self._vector_size = 1536  # Default fallback
        return self._vector_size

    def retrieve(self, embedding: list[float]) -> list[str]:
        import time

        from qdrant_client.http.models import Distance, VectorParams

        # Try to access the collection, create if it doesn't exist
        collection_exists = True

        try:
            collection_info = self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' exists with {collection_info.points_count} points")
        except Exception as e:
            # Collection doesn't exist - we'll create it
            collection_exists = False
            print(f"Collection does not exist, will create: {e}")

        # Create collection if it doesn't exist with correct dimensions
        if not collection_exists:
            try:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=len(embedding), distance=Distance.COSINE
                    ),  # Use the size of the embedding we're receiving
                )
                time.sleep(0.5)  # Brief pause to ensure creation
                print(f"Created new collection: {self.collection_name}")
            except Exception as e:
                # If collection already exists with correct params, continue
                if "already exists" not in str(e):
                    print(f"Error creating collection: {e}")
                    raise e

        # Add a small delay to ensure collection is ready
        time.sleep(0.1)

        try:
            # ADD LOGGING to verify vectors exist
            try:
                collection_info = self.client.get_collection(self.collection_name)
                print(f"Collection '{self.collection_name}' exists with {collection_info.points_count} points")
            except Exception as e:
                print(f"Error getting collection info: {e}")

            # INCREASE top_k to at least 8
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                limit=8,  # Increased from 5 to 8
            )

            # Extract text, source, and heading from payloads
            results = []
            for h in hits:
                if h.payload and "text" in h.payload:
                    # For now, just return the text content
                    # Later we can extend to return structured objects with source info
                    results.append(h.payload["text"])

            # ADD LOGGING as requested
            print("QUERY:", embedding[:10])  # First 10 elements of embedding vector
            print("DOC COUNT:", len(results))
            for i, result in enumerate(results[:2]):
                print(result[:200] + "..." if len(result) > 200 else result)

            # ADD LOGGING
            print(f"Retrieval query vector length: {len(embedding)}")
            print(f"Retrieved {len(results)} documents from collection")
            for i, result in enumerate(results[:3]):  # Preview first 3 chunks
                preview = result[:100] + "..." if len(result) > 100 else result
                print(f"Chunk {i+1} preview: {preview}")

            return results
        except Exception as e:
            print(f"Error during search: {e}")
            return []  # Return empty list if search fails

    async def generate_embedding(self, text: str) -> list[float]:
        # Handle potential long texts by truncating to model's max length
        # Most embedding models have limits around 8192 tokens
        max_length = 8000  # Conservative limit
        if len(text) > max_length:
            text = text[:max_length]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": settings.EMBEDDING_MODEL, "input": text},
                timeout=30.0,  # Add a timeout for the request
            )
            response.raise_for_status()
            data = response.json()
            embedding = data["data"][0]["embedding"]
            print(f"Generated embedding with length: {len(embedding)} for model: {settings.EMBEDDING_MODEL}")
            return embedding

    async def generate_rag_response(
        self, user_query: str, retrieved_docs: list[str]  # Note: retrieved_docs from original call is ignored now
    ) -> str:
        # ENFORCE RETRIEVAL FOR EVERY QUERY, even vague ones
        # Expand vague queries internally for better retrieval
        expanded_query = user_query

        # List of vague queries that need expansion
        vague_indicators = [
            "tell me about", "what does this", "this chapter", "this module",
            "this topic", "this section", "this concept", "this idea",
            "this book", "the book", "book", "this", "that", "it", "they"
        ]

        is_vague_query = any(indicator in user_query.lower() for indicator in vague_indicators)

        if is_vague_query:
            expanded_query = user_query + " book content chapter explanation"

        # For "Explain:" queries, use the text after the prefix for direct retrieval
        if user_query.strip().lower().startswith("explain:"):
            explain_text = user_query.strip()[8:].strip()  # Strip "Explain:" prefix
            print(f"Explain query detected. Original: '{user_query}', Extracted text: '{explain_text}'")

            if explain_text:
                # Use highlighted text directly as retrieval query - DO NOT bypass retriever
                explain_embedding = await self.generate_embedding(explain_text)
                explain_docs = self.retrieve(explain_embedding)  # DO NOT rewrite the query
                retrieved_chunks = explain_docs
            else:
                # Even for empty explain, ensure retrieval happens with original query
                expanded_embedding = await self.generate_embedding(expanded_query)
                expanded_docs = self.retrieve(expanded_embedding)
                retrieved_chunks = expanded_docs
        else:
            # Always run retrieval with expanded query
            expanded_embedding = await self.generate_embedding(expanded_query)
            expanded_docs = self.retrieve(expanded_embedding)
            retrieved_chunks = expanded_docs

        # ADD LOGGING
        print(f"Original query: '{user_query}'")
        print(f"Expanded query: '{expanded_query}'")
        print(f"Number of retrieved chunks: {len(retrieved_chunks)}")

        # ONLY return "not covered in the book" IF retrieved_chunks.length == 0
        if len(retrieved_chunks) == 0:
            print("No chunks retrieved - returning fallback message")
            # Return the exact fallback message
            fallback_response = "This information is not covered in the book."
            return fallback_response
        else:
            print("Chunks retrieved - proceeding with LLM response")
            # If chunks exist, the LLM MUST answer using them
            context = "\n\n".join(retrieved_chunks)

            # Create the strict system prompt that enforces ALL rules
            system_prompt = (
                "You are a RAG assistant for the \"Documentation Book\". "
                "You ONLY answer using the provided book content. "
                "EVERY user query refers to this book - DO NOT ask which book. "
                "DO NOT answer from general knowledge. "
                "Answer the user's query using ONLY the provided book content below.\n\n"
                + context
            )

            messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {"role": "user", "content": user_query},
            ]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": settings.CHAT_MODEL, "messages": messages},
                timeout=60.0,  # Add a timeout for the request
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


rag_service = RAGService()
