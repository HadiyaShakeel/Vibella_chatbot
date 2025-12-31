from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "vibella_db"
COLLECTION_NAME = "conversations"

client = AsyncIOMotorClient(MONGODB_URL)
database = client[DATABASE_NAME]
conversations_collection = database[COLLECTION_NAME]

sync_client = MongoClient(MONGODB_URL)
sync_database = sync_client[DATABASE_NAME]

def init_db():
    """
    Initialize MongoDB database and create indexes
    This runs once when the server starts
    """
    try:
        sync_database[COLLECTION_NAME].create_index("timestamp")
        print(" MongoDB initialized successfully")
        print(f" Database: {DATABASE_NAME}")
        print(f" Collection: {COLLECTION_NAME}")
    except Exception as e:
        print(f" MongoDB initialization warning: {e}")

async def save_conversation(user_message: str, ai_response: str, image_data: str = None):
    conversation = {
        "user_message": user_message,
        "ai_response": ai_response,
        "timestamp": datetime.utcnow(),
        "has_image": image_data is not None,  
        "image_data": image_data if image_data else None  
    }
    
    result = await conversations_collection.insert_one(conversation)
    return str(result.inserted_id)

async def get_recent_conversations(limit: int = 10, include_images: bool = False):
    projection = {"image_data": 0} if not include_images else {}
    
    cursor = conversations_collection.find({}, projection).sort("timestamp", -1).limit(limit)
    conversations = await cursor.to_list(length=limit)
    
    
    for conv in conversations:
        conv["_id"] = str(conv["_id"])
    
    return conversations

async def get_conversation_count():
    return await conversations_collection.count_documents({})

def close_db():
    client.close()
    sync_client.close()