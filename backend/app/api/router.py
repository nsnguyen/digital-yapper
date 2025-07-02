from fastapi import APIRouter

from app.api.endpoints import data, chat

api_router = APIRouter()
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# Add a status endpoint
@api_router.get("/status", tags=["system"])
async def get_status():
    """
    Get system status information
    """
    return {
        "status": "online",
        "version": "0.1.0",
        "timestamp": "2023-09-15T12:00:00Z"
    }
