from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    question: str
    conversation_id: Optional[UUID] = None
    selected_text: Optional[str] = None

class Citation(BaseModel):
    source: str
    heading: Optional[str] = None
    chunk_id: Optional[int] = None

class Message(BaseModel):
    role: str # 'user' or 'assistant'
    content: str
    citations: Optional[List[Citation]] = None

class Conversation(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    messages: List[Message] = []
