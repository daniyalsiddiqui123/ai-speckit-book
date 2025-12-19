from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from openai import OpenAI
from core.config import get_settings

settings = get_settings()

class RAGService:
    def __init__(self):
        self.qdrant_client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        self.openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.collection_name = "docusaurus_book"
        self.qwen_embedding_model = "Qwen/text-embedding-l-1024"
        self.chat_model = "google/gemini-flash-1.5" # Or another suitable model

    def get_embedding(self, text: str) -> List[float]:
        """Generates an embedding for the given text."""
        response = self.openrouter_client.embeddings.create(
            model=self.qwen_embedding_model,
            input=text
        )
        return response.data[0].embedding

    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieves relevant document chunks from Qdrant based on the query."""
        query_embedding = self.get_embedding(query)
        
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )
        
        context = []
        for hit in search_result:
            context.append(hit.payload)
        return context

    def generate_response(self, question: str, context_chunks: List[Dict[str, Any]]) -> Any:
        """Generates a response using ChatKit (OpenRouter LLM) based on context."""
        formatted_context = ""
        citations = []
        
        for i, chunk in enumerate(context_chunks):
            formatted_context += f"Source {i+1} (file: {chunk.get('source')}, heading: {chunk.get('heading')}):\n"
            formatted_context += f"{chunk.get('text')}\n\n"
            citations.append({
                "source": chunk.get('source'),
                "heading": chunk.get('heading'),
                "chunk_id": chunk.get('chunk_id')
            })

        prompt = f"""
        You are an expert assistant for the "Physical AI" textbook.
        Answer the user's question based *only* on the following context.
        If the answer is not in the context, respond with "This is not covered in the book.".
        Include citations from the context's metadata. Cite relevant sources by their number (e.g., [Source 1]).

        Context:
        ---
        {formatted_context}
        ---

        Question: {question}
        """

        stream = self.openrouter_client.chat.completions.create(
            model=self.chat_model,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        
        # Yield both content chunks and final citations
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield {"type": "chunk", "content": content}
        
        yield {"type": "citation", "sources": citations}


rag_service = RAGService()
