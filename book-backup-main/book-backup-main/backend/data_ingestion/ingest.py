import os
import glob
import httpx
from pathlib import Path
import re
from qdrant_client import QdrantClient, models
from markdown_it import MarkdownIt
from typing import Optional

# Load settings from environment variables
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "dev-qdrant-key")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "dev-openrouter-key")
COLLECTION_NAME = "docusaurus_book"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen/qwen3-embedding-8b")  # Use same model as in config

# Determine vector size based on the model
if "text-embedding-3-large" in EMBEDDING_MODEL:
    VECTOR_SIZE = 3072
elif "text-embedding-3-small" in EMBEDDING_MODEL:
    VECTOR_SIZE = 1536
elif "text-embedding-ada" in EMBEDDING_MODEL:
    VECTOR_SIZE = 1536
elif "qwen3-embedding-8b" in EMBEDDING_MODEL:
    VECTOR_SIZE = 4096  # Qwen3-embedding-8b produces 4096-dim vectors
elif "qwen" in EMBEDDING_MODEL.lower():
    VECTOR_SIZE = 1024  # Default for other Qwen models
else:
    # Default fallback
    VECTOR_SIZE = 1536

qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def get_embedding(text: str) -> list[float]:
    """Generates an embedding for the given text using the embedding model via OpenRouter."""
    # Handle potential long texts by truncating to model's max length
    # Most embedding models have limits around 8192 tokens
    max_length = 8000  # Conservative limit
    if len(text) > max_length:
        text = text[:max_length]

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }

    with httpx.Client() as client:
        response = client.post(
            "https://openrouter.ai/api/v1/embeddings",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["embedding"]

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


def ingest_documents(docs_path: str = "../my-website/docs"):
    print(f"Starting ingestion from: {docs_path}")
    print(f"Current working directory: {os.getcwd()}")

    # Check if docs path exists
    if not os.path.exists(docs_path):
        print(f"Error: Documentation path does not exist: {docs_path}")
        print("Please make sure your documentation is in the correct location.")
        print("Expected location relative to backend/: ../../my-website/docs")
        print("Make sure you're running this script from the backend directory.")
        return

    # Count markdown files to process
    markdown_files = glob.glob(os.path.join(docs_path, "**/*.md"), recursive=True)
    markdown_files.extend(glob.glob(os.path.join(docs_path, "**/*.mdx"), recursive=True))
    print(f"Found {len(markdown_files)} markdown files to process.")

    if not markdown_files:
        print("No markdown files found in the documentation directory.")
        print(f"Available files in {docs_path}:")
        try:
            for root, dirs, files in os.walk(docs_path):
                for file in files:
                    if file.endswith(('.md', '.mdx')):
                        print(f"  - {os.path.join(root, file)}")
        except Exception as e:
            print(f"Error listing directory: {e}")
        return

    # Check Qdrant connection
    try:
        # Test connection to Qdrant
        qdrant_client.get_collections()
        print("Successfully connected to Qdrant server.")
    except Exception as e:
        print(f"Error connecting to Qdrant server: {e}")
        print("Make sure Qdrant is running before running this script.")
        print("You can run Qdrant locally using Docker:")
        print("  docker run -d --name qdrant -p 6333:6333 qdrant/qdrant")
        print("Or use Qdrant Cloud and update your .env file accordingly.")
        return

    # Ensure Qdrant collection exists
    try:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
        print(f"Collection '{COLLECTION_NAME}' recreated.")
    except Exception as e:
        print(f"Could not recreate collection, might already exist: {e}")

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
