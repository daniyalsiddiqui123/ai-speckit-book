from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from backend.api.deps import get_db
from backend.schemas import chat as chat_schemas
from backend.services.chat_service import chat_service
from backend.services.rag_service import rag_service
from backend.models import Conversation as DBConversation


router = APIRouter()

@router.post("/chat", response_model=chat_schemas.Conversation)
async def chat_with_rag(
    message: chat_schemas.ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        # Create or retrieve conversation
        if message.conversation_id:
            conversation = chat_service.get_conversation(db, message.conversation_id)
            # Remove user_id check since we're not authenticating users
            if not conversation:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
        else:
            # For anonymous users, create a conversation with no user_id (NULL)
            conversation = chat_service.create_conversation(db, None, message.question)

        # Save user message
        chat_service.create_message(db, UUID(str(conversation.id)), "user", message.question)

        # Generate embedding for user query
        query_embedding = await rag_service.generate_embedding(message.question)

        # Retrieve relevant documents
        retrieved_docs = rag_service.retrieve(query_embedding)

        # Generate RAG response
        ai_response_content = await rag_service.generate_rag_response(message.question, retrieved_docs)

        # Save AI message
        chat_service.create_message(db, UUID(str(conversation.id)), "assistant", ai_response_content)

        # Fetch all messages for the conversation to return the full history
        messages = chat_service.get_messages_for_conversation(db, UUID(str(conversation.id)))

        # Create a response object that matches the schema
        from backend.schemas.chat import Conversation as ConversationSchema
        response_conversation = ConversationSchema(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            messages=messages
        )

        return response_conversation

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


