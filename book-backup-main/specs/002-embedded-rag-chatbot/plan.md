# Technical Plan: Embedded RAG Chatbot

**Feature**: Embedded RAG Chatbot
**Branch**: `002-embedded-rag-chatbot`

## 1. High-Level System Architecture

```
+-----------------------------+      +------------------------------+      +---------------------------+
| Docusaurus Frontend (React) |<---->|      FastAPI Backend         |<---->|   Neon Serverless Postgres|
| - Chatbot UI Component      |      |      (Python)                |      |   - User accounts         |
| - Text Selection Logic      |      +------------------------------+      |   - Chat history          |
+-----------------------------+                ^                             +---------------------------+
          |                                    |
          | (User Query)                       | (Vector Search)
          v                                    v
+-----------------------------+      +------------------------------+      +---------------------------+
|      ChatKit SDK            |<---->|      Qdrant Cloud            |<---->|   Embedding Pipeline      |
| - Agent Orchestration       |      |      (Vector DB)             |      |   (OpenRouter - Qwen)     |
+-----------------------------+      +------------------------------+      +---------------------------+
```

**Data & Logic Flow:**

1.  **User Interaction**: A user interacts with the Chatbot UI in the Docusaurus frontend. They can either type a question directly or select text and then ask a question.
2.  **API Request**: The frontend sends a request to the FastAPI backend.
    *   If text is selected, the selected text is included in the payload.
    *   The request is authenticated using a JWT access token.
3.  **Authentication**: The backend validates the JWT. If a user is authenticated, their chat history is retrieved/persisted.
4.  **Contextual RAG vs. Global RAG**:
    *   **Selected Text (Contextual RAG)**: If the payload includes selected text, this text is sent *directly* to the `ChatKit` SDK as the context. The global vector search is **bypassed**.
    *   **No Selection (Global RAG)**: If no text is selected, the user's query is sent to the retrieval pipeline.
5.  **Retrieval Pipeline (Global RAG only)**:
    *   The user's query is converted into an embedding using the Qwen model via OpenRouter.
    *   The embedding is used to perform a similarity search against the Qdrant vector collection.
    *   Relevant document chunks are retrieved.
6.  **Generation**: The retrieved chunks (from Global RAG) or the selected text (from Contextual RAG) are passed to the `ChatKit` SDK as context along with the user's question. The SDK orchestrates the call to the OpenRouter LLM to generate a response.
7.  **Response Streaming**: The FastAPI backend streams the response from the LLM back to the frontend.
8.  **Persistence**: The conversation (question, answer, citations) is saved to the Neon Postgres database for authenticated users.

## 2. Backend Folder Structure (FastAPI)

```
backend/
├── main.py             # FastAPI app initialization
├── .env                # Environment variables
├── requirements.txt    # Python dependencies
├── core/
│   ├── config.py       # Configuration loading
│   └── security.py     # JWT handling, password hashing
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py       # /signup, /login endpoints
│   │   └── chat.py       # /chat endpoint for the RAG bot
│   └── deps.py         # FastAPI dependencies (e.g., get_current_user)
├── schemas/
│   ├── __init__.py
│   ├── user.py         # Pydantic models for User
│   ├── token.py        # Pydantic models for JWT
│   └── chat.py         # Pydantic models for chat messages
├── services/
│   ├── __init__.py
│   ├── user_service.py # User CRUD operations
│   ├── chat_service.py # Chat history CRUD
│   └── rag_service.py  # Handles RAG logic, embedding, and generation
└── data_ingestion/
    ├── __init__.py
    └── ingest.py       # Script to read Docusaurus content, chunk it, and store in Qdrant
```

## 3. Frontend Integration Approach

1.  **Chatbot Component**:
    *   A new React component, `Chatbot.tsx`, will be created in `my-website/src/components/`.
    *   This component will manage the chat UI (messages, input field, etc.) and its state (visibility, loading, etc.).
2.  **Global Integration**:
    *   The `Chatbot.tsx` component will be added to the Docusaurus root layout (`my-website/src/theme/Layout/index.js` or swizzled equivalent). This ensures it is available on every page.
    *   It will be rendered as a floating action button or a fixed icon that, when clicked, opens the chat interface.
3.  **Text Selection Handling**:
    *   A global event listener for `mouseup` will be added in the root layout.
    *   When the event fires, it will check `window.getSelection().toString()`. If text is selected, a small "Ask Chatbot" button will appear near the selected text.
    *   Clicking this button will open the chatbot and pass the selected text into its state.
4.  **State Management**:
    *   React Context or a simple state management library (like Zustand) will be used to manage the chatbot's state, including the selected text, user authentication status, and current conversation.
5.  **API Client**:
    *   A simple API client module will be created to handle authenticated requests to the FastAPI backend (e.g., using `fetch` or `axios`). It will manage attaching the JWT to headers.

## 4. API Contracts

### Authentication

*   **Endpoint**: `POST /api/auth/signup`
    *   **Request Body**: `{ "email": "user@example.com", "password": "strongpassword" }`
    *   **Response**: `{ "id": 1, "email": "user@example.com" }`
*   **Endpoint**: `POST /api/auth/login`
    *   **Request Body**: `{ "username": "user@example.com", "password": "strongpassword" }` (using form data for OAuth2PasswordRequestForm)
    *   **Response**: `{ "access_token": "...", "refresh_token": "...", "token_type": "bearer" }`

### Chat

*   **Endpoint**: `POST /api/chat`
    *   **Authentication**: Required (JWT Bearer Token)
    *   **Request Body**:
        ```json
        {
          "question": "What is inverse kinematics?",
          "conversation_id": "optional-uuid-to-continue-thread",
          "selected_text": "optional-string-of-user-selected-text"
        }
        ```
    *   **Response**: A `StreamingResponse` with server-sent events.
        *   **Event `data`**: `{ "type": "chunk", "content": "Inverse kinematics is..." }`
        *   **Event `data`**: `{ "type": "citation", "sources": ["/docs/chapter5.md#section-2"] }`
        *   **Event `end`**: `{ "type": "end", "conversation_id": "new-uuid" }`

## 5. Database Schema (Neon Postgres)

```sql
CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "email" VARCHAR(255) UNIQUE NOT NULL,
  "hashed_password" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "conversations" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "user_id" INTEGER NOT NULL REFERENCES "users"("id") ON DELETE CASCADE,
  "title" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "messages" (
  "id" SERIAL PRIMARY KEY,
  "conversation_id" UUID NOT NULL REFERENCES "conversations"("id") ON DELETE CASCADE,
  "role" VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
  "content" TEXT NOT NULL,
  "citations" JSONB, -- Store source files/sections
  "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## 6. Qdrant Vector Collection Schema

*   **Collection Name**: `docusaurus_book`
*   **Vector Parameters**:
    *   `size`: (Determined by Qwen embedding model, e.g., 1024)
    *   `distance`: `Cosine`
*   **Payload Schema**: Each vector will have a payload containing its metadata.
    ```json
    {
      "text": "The full text of the document chunk.",
      "source": "/docs/chapter1.md",
      "heading": "Introduction to Robotics", // The nearest preceding heading
      "chunk_id": "integer-index-of-chunk-in-source-file"
    }
    ```

## 7. Embedding + Retrieval Pipeline Flow

1.  **Offline Ingestion (`data_ingestion/ingest.py`)**:
    *   The script recursively scans the `my-website/docs` directory for `.md` and `.mdx` files.
    *   Each file is read and split into smaller chunks (e.g., by paragraph or a fixed token size).
    *   For each chunk, the script calls the OpenRouter API endpoint for the Qwen embedding model to get its vector representation.
    *   The chunk's text, vector, and metadata (source file, heading) are uploaded to the Qdrant collection.
    *   This script will need to be run whenever the book content is updated.
2.  **Online Retrieval (Global RAG in `services/rag_service.py`)**:
    *   The user's query is received.
    *   A request is made to the Qwen embedding model via OpenRouter to get the query vector.
    *   The `rag_service` uses the Qdrant client to search the `docusaurus_book` collection with the query vector.
    *   The top `k` (e.g., 3-5) most similar chunks are retrieved.
    *   The `text` from these chunks is concatenated to form the context.

## 8. Auth Flow (JWT)

1.  **Signup**: A new user is created in the `users` table with a hashed password.
2.  **Login**: The user provides their email and password. The backend verifies the credentials.
3.  **Token Generation**: Upon successful login, the backend generates a short-lived `access_token` and a long-lived `refresh_token`.
4.  **Authenticated Requests**: The frontend stores the tokens (e.g., in `localStorage`) and sends the `access_token` in the `Authorization: Bearer <token>` header for all protected endpoints like `/api/chat`.
5.  **Token Refresh**: When the `access_token` expires, the frontend can use the `refresh_token` to get a new pair of tokens without requiring the user to log in again.

## 9. Agent Orchestration Flow using ChatKit

The `services/rag_service.py` will be the primary place where `ChatKit` is used.

```python
# Psuedocode for rag_service.py

from chatkit import ChatKit

# Initialize ChatKit with OpenRouter credentials
chatkit = ChatKit(api_key=OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")

def generate_response(question: str, context: str):
    prompt = f"""
    You are an expert assistant for the "Physical AI" textbook.
    Answer the user's question based *only* on the following context.
    If the answer is not in the context, respond with "This is not covered in the book.".
    Include citations from the context's metadata.

    Context:
    ---
    {context}
    ---

    Question: {question}
    """

    stream = chatkit.chat.completions.create(
        model="google/gemini-flash-1.5", # Or another suitable model from OpenRouter
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    for chunk in stream:
        # Yield chunks for streaming response
        yield chunk.choices[0].delta.content
```

**Key Logic**: The `rag_service` will be responsible for preparing the `context` string (either from Qdrant or from the user's selected text) and then passing it into the prompt for the ChatKit SDK.

## 10. Environment Variable Definitions

**.env file for the backend:**

```
# Database
DATABASE_URL="postgresql://user:password@host:port/dbname"

# JWT
SECRET_KEY="a-very-secret-key-for-jwt"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OpenRouter
OPENROUTER_API_KEY="your-openrouter-api-key"

# Qdrant
QDRANT_URL="your-qdrant-cloud-url"
QDRANT_API_KEY="your-qdrant-api-key"

# Frontend
# The URL of the Docusaurus app, for CORS
CLIENT_ORIGIN_URL="http://localhost:3000"
```
