---
id: 0001
title: Define Embedded RAG Chatbot Spec
stage: spec
date: 2025-12-18
surface: agent
model: gemini-cli
feature: 002-embedded-rag-chatbot
branch: 002-embedded-rag-chatbot
user: "N/A"
command: "/sp.specify"
labels: ["rag", "chatbot", "docusaurus"]
links:
  spec: "specs/002-embedded-rag-chatbot/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-embedded-rag-chatbot/spec.md"
  - "specs/002-embedded-rag-chatbot/checklists/requirements.md"
tests:
  - "N/A"
---

## Prompt

You are a senior AI systems architect. Define the complete specification for an Embedded Retrieval-Augmented Generation (RAG) chatbot inside a Docusaurus book project. PROJECT GOAL: Build a chatbot that answers questions strictly from the book’s content and supports answering questions based on user-selected text as well. TECH STACK (FIXED): - Frontend: Docusaurus (React) - Backend: FastAPI (Python) - RAG Orchestration: OpenAI Agents / ChatKit SDK - LLM Access: OpenRouter API - Embeddings: Qwen embedding model (via OpenRouter) - Vector DB: Qdrant Cloud (Free Tier) - Relational DB: Neon Serverless Postgres - Auth: JWT (access + refresh tokens) CORE FUNCTIONAL REQUIREMENTS: 1. Chatbot must only answer using book content. 2. If the user highlights/selects text: - The chatbot MUST answer using only that selected text (plus minimal local context). 3. If no text is selected: - Use global RAG over the entire book. 4. If the answer is not found in context: - Respond exactly: "This is not covered in the book." 5. Responses must be streamed. 6. Each response must include citations (file + section). 7. Chat history must persist for authenticated users. NON-FUNCTIONAL REQUIREMENTS: - No hallucinations. - No external internet search. - Scalable, modular architecture. - Clean separation of ingestion, retrieval, and generation. OUTPUT: Produce a clear, structured system specification including: - User flows - Data flow - RAG behavior rules - Agent behavior rules - Security constraints

## Response snapshot

I have created a new feature branch `002-embedded-rag-chatbot` and generated the initial specification file at `specs/002-embedded-rag-chatbot/spec.md`. I also created a requirements checklist at `specs/002-embedded-rag-chatbot/checklists/requirements.md`.

The specification is complete and ready for review.

## Outcome

- ✅ Impact: Created a detailed specification for the Embedded RAG Chatbot feature.
- 🧪 Tests: N/A
- 📁 Files: 
  - specs/002-embedded-rag-chatbot/spec.md
  - specs/002-embedded-rag-chatbot/checklists/requirements.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The process of creating the specification was straightforward. The user provided a very detailed prompt which made it easy to generate the required artifacts. The issues with the scripts creating the files in the correct directories was a bit of a setback, but I was able to work around it by creating the files manually.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-new-feature.sh` and `create-phr.sh` scripts did not correctly handle the file paths when the agent's working directory was not the same as the project's root directory.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Fix the pathing issues in the shell scripts.
