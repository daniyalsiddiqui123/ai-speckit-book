from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID
import json

from models.conversation import Conversation
from models.message import Message
from schemas.chat import Message as MessageSchema, Citation, Conversation as ChatSchemaConversation

class ChatService:
    def create_conversation(self, db: Session, user_id, initial_question: str) -> Conversation:
        conversation = Conversation(user_id=user_id, title=initial_question[:100]) # Use first 100 chars as title
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation

    def get_conversation(self, db: Session, conversation_id: UUID) -> Optional[ChatSchemaConversation]:
        db_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not db_conversation:
            return None

        messages = self.get_messages_for_conversation(db, UUID(str(db_conversation.id)))
        return ChatSchemaConversation(
            id=db_conversation.id,
            user_id=db_conversation.user_id,
            title=db_conversation.title,
            messages=messages
        )

    def get_user_conversations(self, db: Session, user_id: int) -> List[ChatSchemaConversation]:
        db_conversations = db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).all()
        conversations = []
        for db_conversation in db_conversations:
            messages = self.get_messages_for_conversation(db, UUID(str(db_conversation.id)))
            conversations.append(ChatSchemaConversation(
                id=db_conversation.id,
                user_id=db_conversation.user_id,
                title=db_conversation.title,
                messages=messages
            ))
        return conversations

    def create_message(self, db: Session, conversation_id: UUID, role: str, content: str, citations: Optional[List[Citation]] = None) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            citations=json.dumps([c.model_dump() for c in citations]) if citations else None
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_messages_for_conversation(self, db: Session, conversation_id: UUID) -> List[MessageSchema]:
        db_messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
        messages = []
        for db_message in db_messages:
            citations = json.loads(db_message.citations) if db_message.citations else None
            messages.append(MessageSchema(
                role=db_message.role,
                content=db_message.content,
                citations=[Citation(**c) for c in citations] if citations else None
            ))
        return messages

chat_service = ChatService()

