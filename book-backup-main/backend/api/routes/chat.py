from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json

from core.database import get_db
from core.config import get_settings
from api.deps import get_current_user
from schemas.chat import ChatRequest, Message, Citation
from schemas.user import User
from services.rag_service import rag_service
from services.chat_service import chat_service

from fastapi_limiter.depends import RateLimiter

settings = get_settings()

router = APIRouter()

@router.post("/chat", dependencies=[Depends(RateLimiter(times=5, seconds=10))]) # 5 requests every 10 seconds
async def chat_endpoint(chat_request: ChatRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Determine context based on selected_text
    context_chunks = []
    if chat_request.selected_text:
        context_chunks.append({"text": chat_request.selected_text, "source": "selected_text", "heading": None, "chunk_id": None})
    else:
        # Global RAG retrieval
        context_chunks = rag_service.retrieve_context(chat_request.question)
        if not context_chunks:
            # Handle case where no context is found for global RAG
            # This should ideally be caught by the LLM prompt, but a safeguard here
            yield json.dumps({"type": "chunk", "content": "This is not covered in the book."}) + "\n"
            yield json.dumps({"type": "end", "conversation_id": None}) + "\n"
            return
    
    # Generate response
    response_generator = rag_service.generate_response(chat_request.question, context_chunks)

    async def event_generator():
        full_response_content = ""
        final_citations = []
        conversation_id = chat_request.conversation_id

        # If it's a new conversation, create one
        if not conversation_id and current_user:
            conversation_id = chat_service.create_conversation(db, current_user.id, chat_request.question).id
            yield json.dumps({"type": "start", "conversation_id": str(conversation_id)}) + "\n"
        
        # Save user message
        if current_user and conversation_id:
            chat_service.create_message(db, conversation_id, "user", chat_request.question)

        try:
            for item in response_generator:
                if item["type"] == "chunk":
                    full_response_content += item["content"]
                    yield json.dumps(item) + "\n"
                elif item["type"] == "citation":
                    final_citations = item["sources"]
                    yield json.dumps(item) + "\n"
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        finally:
            # Save assistant message
            if current_user and conversation_id and full_response_content:
                chat_service.create_message(db, conversation_id, "assistant", full_response_content, final_citations)
            
            yield json.dumps({"type": "end", "conversation_id": str(conversation_id)}) + "\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
