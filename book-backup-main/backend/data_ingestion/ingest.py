import os
import glob
from pathlib import Path
import re
from qdrant_client import QdrantClient, models
from openai import OpenAI # Using openai client for OpenRouter
from markdown_it import MarkdownIt
from typing import Optional

# Placeholder for settings (will be imported from core.config)
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
COLLECTION_NAME = "docusaurus_book"
VECTOR_SIZE = 1024 # This should match the Qwen embedding model output size (e.g., Qwen/text-embedding-l-1024)
QWEN_EMBEDDING_MODEL = "Qwen/text-embedding-l-1024" # Example Qwen model on OpenRouter

qdrant_client = QdrantClient(
    url=QDRANT_URL, 
    api_key=QDRANT_API_KEY
)

# Initialize OpenRouter client
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using the Qwen model via OpenRouter."""
    response = openrouter_client.embeddings.create(
        model=QWEN_EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Splits text into chunks of a specified size with overlap.
    Aims to split by paragraphs first, then by sentences if paragraph is too large.
    """
    chunks = []
    paragraphs = text.split('\n\n')

    for para in paragraphs:
        if len(para.split()) > chunk_size:  # If paragraph is too long, try sentence splitting
            sentences = re.split(r'(?<=[.!?])\s+', para)
            current_chunk = []
            for sentence in sentences:
                if len(' '.join(current_chunk + [sentence]).split()) > chunk_size:
                    if current_chunk:
                        chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                else:
                    current_chunk.append(sentence)
            if current_chunk:
                chunks.append(' '.join(current_chunk))
        else: # Add paragraph as a whole chunk
            chunks.append(para)

    # Further split if any chunk is still too large or ensure minimum size
    final_chunks = []
    for chunk in chunks:
        words = chunk.split()
        if len(words) > chunk_size:
            for i in range(0, len(words), chunk_size - overlap):
                final_chunks.append(' '.join(words[i:i + chunk_size]))
        else:
            final_chunks.append(chunk)

    return [c.strip() for c in final_chunks if c.strip()]

def get_nearest_heading(content: str, start_pos: int) -> Optional[str]:
    """
    Extracts the nearest preceding Markdown heading for a given position.
    """
    md = MarkdownIt()
    tokens = md.parse(content)
    
    last_heading = None
    for token in tokens:
        if token.map and token.map[0] < start_pos:
            if token.type == 'heading_open':
                # The next token is inline and contains the heading text
                for next_token in tokens[tokens.index(token)+1:]:
                    if next_token.type == 'inline':
                        last_heading = next_token.content
                        break
        elif token.map and token.map[0] >= start_pos:
            break
    return last_heading


def ingest_documents(docs_path: str = "../../my-website/docs"):
    print(f"Starting ingestion from: {docs_path}")
    
    # Ensure Qdrant collection exists
    try:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' recreated.")
    except Exception as e:
        print(f"Could not recreate collection, might already exist: {e}")

    markdown_files = glob.glob(os.path.join(docs_path, "**/*.md"), recursive=True)
    markdown_files.extend(glob.glob(os.path.join(docs_path, "**/*.mdx"), recursive=True))

    points = []
    for file_path in markdown_files:
        print(f"Processing file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = chunk_text(content)
        for i, chunk in enumerate(chunks):
            print(f"  Chunk {i+1}: {chunk[:100]}...") # Print first 100 chars of chunk
            embedding = get_embedding(chunk)
            
            # Get nearest heading for metadata
            # Approximate start_pos for simplicity, more accurate parsing needed for production
            start_pos = content.find(chunk) 
            heading = get_nearest_heading(content, start_pos)
            
            payload = {
                "text": chunk,
                "source": os.path.relpath(file_path, docs_path), # Relative path for citation
                "heading": heading,
                "chunk_id": i
            }
            
            points.append(
                models.PointStruct(
                    id=f"{os.path.basename(file_path)}-{i}", # Unique ID for each chunk
                    vector=embedding,
                    payload=payload
                )
            )
            
            if len(points) >= 100: # Batch upload for efficiency
                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME,
                    wait=True,
                    points=points
                )
                points = []
            
    if points: # Upload any remaining points
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=points
        )
            
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_documents()
