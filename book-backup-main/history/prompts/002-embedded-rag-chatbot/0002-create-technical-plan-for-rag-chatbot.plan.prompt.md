---
id: 0002
title: Create Technical Plan for RAG Chatbot
stage: plan
date: 2025-12-18
surface: agent
model: gemini-cli
feature: 002-embedded-rag-chatbot
branch: 002-embedded-rag-chatbot
user: "N/A"
command: "/sp.plan"
labels: ["rag", "chatbot", "docusaurus", "fastapi", "qdrant", "postgres"]
links:
  spec: "specs/002-embedded-rag-chatbot/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-embedded-rag-chatbot/plan.md"
tests:
  - "N/A"
---

## Prompt

You are a lead full-stack engineer.

Using the approved specification, create a detailed technical plan for implementing the Embedded RAG Chatbot.

REQUIRED OUTPUT SECTIONS:
1. High-level system architecture diagram (text-based).
2. Backend folder structure (FastAPI).
3. Frontend integration approach for Docusaurus.
4. API contracts (endpoint names, inputs, outputs).
5. Database schema (Neon Postgres).
6. Qdrant vector collection schema.
7. Embedding + retrieval pipeline flow.
8. Auth flow (JWT).
9. Agent orchestration flow using ChatKit.
10. Environment variable definitions.

CONSTRAINTS:
- Must use Qwen embeddings via OpenRouter.
- Must support selected-text RAG and global RAG.
- Must be production-ready.
- Must clearly show how selected text bypasses global retrieval.

## Response snapshot

I have created a detailed technical plan for the Embedded RAG Chatbot feature and saved it to `specs/002-embedded-rag-chatbot/plan.md`.

The plan includes the system architecture, backend and frontend structure, API contracts, database schemas, and implementation details for the retrieval and authentication flows.

## Outcome

- ✅ Impact: Created a comprehensive technical plan for the Embedded RAG Chatbot feature.
- 🧪 Tests: N/A
- 📁 Files: 
  - specs/002-embedded-rag-chatbot/plan.md
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The detailed specification made it straightforward to create a thorough technical plan. The architecture is designed to be modular and scalable, cleanly separating the concerns of data ingestion, retrieval, and generation. The dual-mode RAG approach is clearly defined.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.sh` script continues to have issues with pathing, requiring manual file creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Fix the pathing issues in the shell scripts.
