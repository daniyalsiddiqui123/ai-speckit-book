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

        # Check the collection's actual vector size
        collection_exists = True
        has_correct_dimension = False

        try:
            collection_info = self.client.get_collection(self.collection_name)
            # Check if the vector dimension matches - using same approach as vector_size property
            actual_vector_size = None
            if hasattr(collection_info.config, "params"):
                params = collection_info.config.params
                # Check for different possible attribute names
                if hasattr(params, "vectors_config"):
                    actual_vector_size = params.vectors_config.size
                elif hasattr(params, "vector_size"):
                    actual_vector_size = params.vector_size
                elif hasattr(params, "size"):
                    actual_vector_size = params.size
                else:
                    # Try to access as dictionary if it's a mapping type
                    try:
                        if hasattr(params, '__getitem__'):
                            if 'vectors_config' in params and hasattr(params['vectors_config'], 'size'):
                                actual_vector_size = params['vectors_config'].size
                            elif 'vector_size' in params:
                                actual_vector_size = params['vector_size']
                    except (TypeError, AttributeError):
                        pass
            else:
                # If we can't determine the actual size, skip the dimension check
                actual_vector_size = len(embedding)  # Assume it matches to continue

            if actual_vector_size and len(embedding) == actual_vector_size:
                has_correct_dimension = True
            else:
                # Vector dimension mismatch - we'll handle this by recreating the collection
                self.client.delete_collection(self.collection_name)
                collection_exists = False
        except Exception as e:
            # Collection doesn't exist - we'll create it
            collection_exists = False
            print(f"Collection does not exist: {e}")

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
            hits = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                limit=5,
            )

            # Extract text, source, and heading from payloads
            results = []
            for h in hits:
                if h.payload and "text" in h.payload:
                    # For now, just return the text content
                    # Later we can extend to return structured objects with source info
                    results.append(h.payload["text"])

            print(f"Retrieved {len(results)} documents from collection")
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
            return data["data"][0]["embedding"]

    async def generate_rag_response(
        self, user_query: str, retrieved_docs: list[str]
    ) -> str:
        context = "\n\n".join(retrieved_docs)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the website and the book's content to answer the user's question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n"
                + context,
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
