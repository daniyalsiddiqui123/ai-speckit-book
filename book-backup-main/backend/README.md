# FastAPI Backend for Embedded RAG Chatbot

This directory contains the FastAPI backend application for the Embedded RAG Chatbot feature.

## Features

- User authentication (signup, login) with JWT (access and refresh tokens).
- Chat endpoint for RAG queries, supporting global and selected-text context.
- Streaming responses from the LLM.
- Persistence of user chat history in a PostgreSQL database.
- Integration with Qdrant Cloud for vector search.
- Integration with OpenRouter API for LLM (Qwen embeddings, Gemini-Flash-1.5 chat model).
- Data ingestion pipeline for Docusaurus markdown content.
- Basic error handling and rate limiting.

## Setup

1.  **Clone the repository**: (If you haven't already)
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>/book-backup-main/backend
    ```

2.  **Create and activate a Python virtual environment**:
    ```bash
    python -m venv venv
    ./venv/Scripts/activate # On Windows
    source venv/bin/activate # On Linux/macOS
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Create a `.env` file in the `backend/` directory based on the provided `.env.example`.
    ```dotenv
    # .env example
    DATABASE_URL="postgresql://user:password@host:port/dbname" # e.g., from Neon Serverless Postgres
    SECRET_KEY="a-very-secret-key-for-jwt-generation" # Generate a strong random key
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    OPENROUTER_API_KEY="sk-or-..." # Your OpenRouter API key
    QDRANT_URL="https://your-qdrant-cloud-url" # Your Qdrant Cloud URL
    QDRANT_API_KEY="your-qdrant-api-key" # Your Qdrant API key
    CLIENT_ORIGIN_URL="http://localhost:3000" # URL of your Docusaurus frontend
    ```
    Ensure you replace placeholder values with your actual credentials and settings.

5.  **Run Database Migrations (Optional, if using Alembic)**:
    This project currently uses `Base.metadata.create_all(bind=engine)` on startup to create tables. For production, consider using Alembic for proper migrations.

6.  **Ingest Docusaurus Documentation**:
    Before running the chat service, you need to ingest your Docusaurus documentation into Qdrant.
    ```bash
    chmod +x ingest.sh # Make the script executable
    ./ingest.sh
    ```
    This script will read markdown files from `../../my-website/docs`, chunk them, generate embeddings using Qwen via OpenRouter, and upload them to your Qdrant instance.

## Running the Application

To start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## Testing

To run backend tests:

```bash
pytest
```
