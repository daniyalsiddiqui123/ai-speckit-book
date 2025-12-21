# Tasks: Embedded RAG Chatbot

**Feature**: Embedded RAG Chatbot

## Phase 1: Project Setup & Foundational Backend

This phase establishes the project structure and core backend components that everything else will depend on.

- [X] T001 Create the backend folder structure as defined in `plan.md`.
- [X] T002 Initialize the FastAPI application in `backend/main.py`.
- [X] T003 [P] Create the Pydantic schemas in `backend/schemas/` for `user.py`, `token.py`, and `chat.py`.
- [X] T004 [P] Implement configuration loading in `backend/core/config.py` to read from a `.env` file.
- [X] T005 Create the `requirements.txt` file and add initial dependencies: `fastapi`, `uvicorn`, `pydantic`, `python-dotenv`.
- [X] T006 Create the `.env.example` file with all variables defined in `plan.md`.

## Phase 2: User Authentication & Database Setup (US3)

This phase implements User Story 3, as it is a dependency for other user stories that require authentication for chat history.

**User Story**: US3 - View and continue past conversations.
**Independent Test**: A user can sign up, log in, receive a JWT, and have their user data stored in the database. Subsequent requests with the JWT correctly identify the user.

- [X] T007 [US3] Add database connection logic to connect to Neon Postgres.
- [X] T008 [US3] Implement the database schema from `plan.md` using SQLAlchemy models or raw SQL in an alembic migration.
- [X] T009 [US3] Implement password hashing and JWT generation/validation logic in `backend/core/security.py`.
- [X] T010 [US3] Create the user creation and retrieval logic in `backend/services/user_service.py`.
- [X] T011 [US3] Implement the `/api/auth/signup` and `/api/auth/login` endpoints in `backend/api/routes/auth.py`.
- [X] T012 [P] [US3] Add `passlib[bcrypt]` and `python-jose[cryptography]` to `requirements.txt`.
- [X] T013 [P] [US3] Create FastAPI dependency `get_current_user` in `backend/api/deps.py`.

## Phase 3: Data Ingestion Pipeline

This phase focuses on creating the script to process and embed the book's content.

- [X] T014 Create the data ingestion script structure in `backend/data_ingestion/ingest.py`.
- [X] T015 [P] Add `qdrant-client` and `openai` (for ChatKit compatibility) to `requirements.txt`.
- [X] T016 Implement logic in `ingest.py` to scan the `my-website/docs` directory.
- [X] T017 Implement text chunking logic within `ingest.py`.
- [X] T018 Implement the connection to Qdrant cloud in `ingest.py`.
- [X] T019 Implement the logic to call the OpenRouter API for Qwen embeddings in `ingest.py`.
- [X] T020 Combine the steps in `ingest.py` to create and upload vectors with their payloads to the Qdrant collection.
- [X] T021 Add a command to `package.json` or a separate shell script to run the ingestion process.

## Phase 4: Core Chat & Global RAG (US1)

This phase implements the primary feature of asking a question against the entire book.

**User Story**: US1 - Ask a question about the book.
**Independent Test**: A user can send a question to the `/api/chat` endpoint and receive a streamed response with citations, generated from a vector search over the entire book.

- [X] T022 [US1] Create the initial `rag_service.py` in `backend/services/`.
- [X] T023 [US1] Implement the global RAG retrieval path: query embedding, Qdrant search, and context assembly in `rag_service.py`.
- [X] T024 [US1] Implement the ChatKit orchestration logic in `rag_service.py` to generate an answer from the retrieved context.
- [X] T025 [US1] Implement the `/api/chat` endpoint in `backend/api/routes/chat.py`.
- [X] T026 [US1] Implement the streaming response logic in the `/api/chat` endpoint.
- [X] T027 [US1] Implement the `chat_service.py` to save and retrieve conversation history from the Postgres database.
- [X] T028 [P] [US1] Create the frontend `Chatbot.tsx` component in `my-website/src/components/`.
- [X] T029 [P] [US1] Add the `Chatbot.tsx` component to the root Docusaurus layout.
- [X] T030 [US1] Implement the frontend API client to make requests to the `/api/chat` endpoint.
- [X] T031 [US1] Implement frontend logic to display the streamed response and citations in the `Chatbot.tsx` UI.

## Phase 5: Selected-Text RAG (US2)

This phase adds the contextual answering capability based on user text selections.

**User Story**: US2 - Ask a question about selected text.
**Independent Test**: A user can select text on the page, ask a question, and the backend will *only* use the selected text as context for the answer, bypassing the vector search.

- [X] T032 [US2] Add a global `mouseup` event listener to the Docusaurus root layout to detect text selection.
- [X] T033 [US2] Implement the small "Ask Chatbot" button that appears near selected text.
- [X] T034 [US2] Modify the `Chatbot.tsx` component to accept and store the `selected_text`.
- [X] T035 [US2] Update the frontend API client to include `selected_text` in the `/api/chat` request payload.
- [X] T036 [US2] Modify the `/api/chat` endpoint in `backend/api/routes/chat.py` to handle the `selected_text` field.
- [X] T037 [US2] In `rag_service.py`, implement the logic branch: if `selected_text` is present, bypass Qdrant and use the provided text as the context for ChatKit.

## Phase 6: Polish & Cross-Cutting Concerns

This final phase addresses testing, documentation, and other non-functional requirements.

- [X] T038 [P] Write unit tests for critical backend logic (e.g., `security.py`, `rag_service.py`).
- [X] T039 [P] Write integration tests for the API endpoints.
- [X] T040 Add comprehensive error handling to the backend services and API routes.
- [X] T041 Implement rate limiting for the API endpoints.
- [X] T042 [P] Create a `README.md` for the `backend` directory explaining setup and how to run the service.
- [X] T043 Refine the frontend `Chatbot.tsx` UI/UX for a polished look and feel.

---

## Dependencies

- **US1 (Global RAG)** depends on **Phase 3 (Ingestion)**.
- **US2 (Selected-Text RAG)** depends on **US1 (Global RAG)** as it modifies the existing chat functionality.
- **US3 (Auth & History)** is a foundational part of the backend but its full value is realized with US1 and US2.

## Implementation Strategy

The implementation will follow the phases outlined above. The Minimum Viable Product (MVP) consists of completing **Phases 1, 2, 3, and 4**, which will deliver the core functionality of a global RAG chatbot with user authentication. Phase 5 and 6 build upon this MVP.
