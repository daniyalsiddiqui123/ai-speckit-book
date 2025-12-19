# Feature Specification: Embedded RAG Chatbot

**Feature Branch**: `002-embedded-rag-chatbot`
**Created**: 2025-12-18
**Status**: Draft
**Input**: User description: "You are a senior AI systems architect. Define the complete specification for an Embedded Retrieval-Augmented Generation (RAG) chatbot inside a Docusaurus book project. PROJECT GOAL: Build a chatbot that answers questions strictly from the book’s content and supports answering questions based on user-selected text as well. TECH STACK (FIXED): - Frontend: Docusaurus (React) - Backend: FastAPI (Python) - RAG Orchestration: OpenAI Agents / ChatKit SDK - LLM Access: OpenRouter API - Embeddings: Qwen embedding model (via OpenRouter) - Vector DB: Qdrant Cloud (Free Tier) - Relational DB: Neon Serverless Postgres - Auth: JWT (access + refresh tokens) CORE FUNCTIONAL REQUIREMENTS: 1. Chatbot must only answer using book content. 2. If the user highlights/selects text: - The chatbot MUST answer using only that selected text (plus minimal local context). 3. If no text is selected: - Use global RAG over the entire book. 4. If the answer is not found in context: - Respond exactly: 'This is not covered in the book.' 5. Responses must be streamed. 6. Each response must include citations (file + section). 7. Chat history must persist for authenticated users. NON-FUNCTIONAL REQUIREMENTS: - No hallucinations. - No external internet search. - Scalable, modular architecture. - Clean separation of ingestion, retrieval, and generation. OUTPUT: Produce a clear, structured system specification including: - User flows - Data flow - RAG behavior rules - Agent behavior rules - Security constraints"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask a question about the book (Priority: P1)

As a reader, I want to ask a question in the chatbot and get a direct answer based on the entire book's content, so that I can quickly find information without searching manually.

**Why this priority**: This is the core functionality of the chatbot and provides the primary value to the user.

**Independent Test**: Can be tested by opening the chatbot, typing a question, and verifying that the answer is relevant, accurate, and sourced from the book.

**Acceptance Scenarios**:

1.  **Given** a user is on any page of the Docusaurus book, **When** they open the chatbot and ask a question relevant to the book's content, **Then** the chatbot streams a response that accurately answers the question and provides citations to the relevant sections of the book.
2.  **Given** a user asks a question whose answer is not in the book, **When** they submit the question, **Then** the chatbot responds with the exact message: "This is not covered in the book."

---

### User Story 2 - Ask a question about selected text (Priority: P2)

As a reader, I want to highlight a specific passage in the book and ask a clarifying question about it, so that I can get a contextual answer focused only on the text I've selected.

**Why this priority**: This provides a more focused and precise way for users to interact with the content, enhancing comprehension.

**Independent Test**: Can be tested by selecting text, triggering the chatbot with the selection, asking a question, and verifying the answer is based only on the selected context.

**Acceptance Scenarios**:

1.  **Given** a user has selected a block of text on a page, **When** they invoke the chatbot and ask a question about the selection, **Then** the chatbot streams a response that answers the question using only the selected text as context.
2.  **Given** a user has selected text and asks a question where the answer is not within that selection, **Then** the chatbot responds with the exact message: "This is not covered in the book."

---

### User Story 3 - View and continue past conversations (Priority: P3)

As an authenticated user, I want to see my previous chat history and be able to continue a past conversation, so that I can pick up where I left off and reference previous answers.

**Why this priority**: This enhances the user experience for logged-in users, providing personalization and continuity.

**Independent Test**: Can be tested by logging in, having a conversation, closing and reopening the chatbot, and verifying the history is present.

**Acceptance Scenarios**:

1.  **Given** an authenticated user has had a previous conversation, **When** they open the chatbot, **Then** their chat history is displayed.
2.  **Given** an authenticated user clicks on a previous conversation, **When** the conversation loads, **Then** they can ask a new question to continue the thread.
3.  **Given** a user is not authenticated, **When** they open the chatbot, **Then** no chat history is loaded.

---

### Edge Cases

-   What happens if the user selects a very large block of text? The system should handle this gracefully, potentially by truncating the context.
-   How does the system handle a user rapidly asking questions? Rate limiting should be in place to prevent abuse.
-   What happens if the underlying book content is updated? The RAG system's knowledge base will need to be re-indexed.
-   How does the system handle code blocks or other formatted text within a user's selection? The context should be preserved as accurately as possible.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: System MUST provide a chat interface within the Docusaurus site.
-   **FR-002**: System MUST answer questions using the book's content as the sole source of truth.
-   **FR-003**: System MUST support two modes of RAG: global (entire book) and local (user-selected text).
-   **FR-004**: System MUST stream responses back to the user in real-time.
-   **FR-005**: System MUST include citations (source file and section) with each answer.
-   **FR-006**: System MUST persist chat history for authenticated users.
-   **FR-007**: System MUST return a specific, predefined message ("This is not covered in the book.") if the answer cannot be found in the provided context.
-   **FR-008**: System MUST provide a mechanism for user authentication (e.g., JWT).
-   **FR-009**: The chatbot should be accessible from all pages of the book.
-   **FR-010**: System MUST have a data ingestion pipeline to process and embed the book's content.

### Key Entities

-   **User**: Represents a reader of the book. Can be authenticated or anonymous. Authenticated users have a persistent chat history.
-   **Chat**: A single conversation thread between a User and the chatbot.
-   **Message**: A single entry in a Chat, either from the User or the Chatbot.
-   **DocumentChunk**: A segment of the book's content that has been processed and stored in the vector database for retrieval.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 95% of questions about the book's content receive a relevant and accurate answer.
-   **SC-002**: For questions asked with selected text, 99% of answers must be based *only* on the provided text selection.
-   **SC-003**: The P95 latency for a streamed response to begin appearing must be under 2 seconds.
-   **SC-004**: For authenticated users, 100% of their chat history is correctly retrieved upon re-opening the chatbot.
-   **SC-005**: The system correctly identifies and responds with "This is not covered in the book." for at least 98% of queries that are genuinely outside the scope of the context.
