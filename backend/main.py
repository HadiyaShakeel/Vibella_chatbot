from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from functools import partial

from database import init_db, close_db, save_conversation, get_recent_conversations, get_conversation_count
from models import ChatRequest, ChatResponse
from langchain_agent import get_vibella_response

app = FastAPI(title="Vibella API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup_event():
    init_db()
    print("✨ Vibella is ready!")

@app.on_event("shutdown")
async def shutdown_event():
    close_db()

@app.get("/")
async def root():
    total = await get_conversation_count()
    return {
        "message": "Vibella API",
        "status": "active",
        "total_conversations": total
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        user_message = request.message.strip()
        if not user_message:
            raise HTTPException(400, "Message cannot be empty")
        
        image_data = request.image
        has_image = image_data is not None
        
        print(f" Message: {user_message[:50]}...")
        if has_image:
            print(f"📸 Image: {len(image_data)} chars")
        
        print(" Calling AI...")
        ai_response = get_vibella_response(user_message, image_data)
        print(f"Response: {ai_response[:100]}...")
        
        print(" Saving...")
        conv_id = await save_conversation(user_message, ai_response, image_data)
        print(f"Saved: {conv_id}")
        
        return ChatResponse(
            response=ai_response,
            timestamp=datetime.utcnow(),
            conversation_id=conv_id,
            has_image=has_image
        )
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(" ERROR:")
        traceback.print_exc()
        raise HTTPException(500, str(e))

@app.get("/history")
async def history(limit: int = 10):
    if not 1 <= limit <= 100:
        raise HTTPException(400, "Limit must be 1-100")
    convs = await get_recent_conversations(limit)
    return {"count": len(convs), "conversations": convs}

@app.get("/stats")
async def stats():
    total = await get_conversation_count()
    return {"total_conversations": total, "database": "MongoDB"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)