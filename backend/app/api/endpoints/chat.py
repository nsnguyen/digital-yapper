from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.models import Conversation, Message
from app.models.chat import ChatMessage, ChatResponse
from app.services.chat_service import NursingChatService
import json
import uuid
from sqlalchemy import select

router = APIRouter()
chat_service = NursingChatService()


@router.post("/")
async def chat(message: ChatMessage, db: AsyncSession = Depends(get_db)):
    print(f"Received chat message: {message.content}")
    # TODO: Get user_id from Microsoft auth token
    user_id = "anonymous"  # Placeholder
    
    # Create or get conversation
    if not message.conversation_id:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(id=conversation_id, user_id=user_id)
        db.add(conversation)
    else:
        conversation_id = message.conversation_id
    
    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content
    )
    db.add(user_message)
    
    # Get AI response
    response = await chat_service.chat(message.content)
    
    # Save AI message
    ai_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=response
    )
    db.add(ai_message)
    
    await db.commit()
    
    return ChatResponse(response=response, conversation_id=conversation_id)

@router.post("/stream")
async def chat_stream(message: ChatMessage, db: AsyncSession = Depends(get_db)):
    print(f"Received chat message for streaming: {message}")
    
    # TODO: Get user_id from Microsoft auth token
    user_id = "anonymous"  # Placeholder
    
    # Create or get conversation
    if not message.conversation_id:
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(id=conversation_id, user_id=user_id)
        db.add(conversation)
        await db.commit()
    else:
        conversation_id = message.conversation_id
    
    # Save user message
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=message.content
    )
    db.add(user_message)
    await db.commit()
    
    async def generate():
        full_response = ""
        async for chunk in chat_service.chat_stream(message.content):
            full_response += chunk
            yield f"data: {json.dumps({'content': chunk, 'conversation_id': conversation_id})}\n\n"
        
        # Save complete AI response
        ai_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response
        )
        db.add(ai_message)
        await db.commit()
        
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.get("/conversations")
async def get_conversations(db: AsyncSession = Depends(get_db)):
    # TODO: Filter by user_id from Microsoft auth
    result = await db.execute(select(Conversation).order_by(Conversation.updated_at.desc()))
    conversations = result.scalars().all()
    return conversations

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    return messages
