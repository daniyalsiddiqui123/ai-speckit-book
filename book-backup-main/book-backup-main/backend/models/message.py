from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.core.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False) # 'user' or 'assistant'
    content = Column(String, nullable=False)
    citations = Column(JSONB) # Store source files/sections
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation_obj = relationship("Conversation", back_populates="messages")
