from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatMessage(BaseModel):
    content: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    
class ConversationResponse(BaseModel):
    id: str
    title: Optional[str]
    created_at: datetime
    
class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime
