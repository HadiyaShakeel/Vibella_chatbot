from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    image: Optional[str] = None  

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Give me a caption for a beach sunset photo",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
            }
        }

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
    conversation_id: Optional[str] = None
    has_image: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Caption: Chasing sunsets and dreams\nHashtags: #sunset #beach #vibes",
                "timestamp": "2024-01-15T10:30:00",
                "conversation_id": "507f1f77bcf86cd799439011",
                "has_image": True
            }
        }

class ConversationHistory(BaseModel):
    id: str = Field(alias="_id")
    user_message: str
    ai_response: str
    timestamp: datetime
    has_image: bool = False

    class Config:
        populate_by_name = True
