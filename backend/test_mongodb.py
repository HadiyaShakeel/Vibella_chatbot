import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime


load_dotenv()

print("Testing MongoDB Connection on Windows...\n")

mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
print(f" Connecting to: {mongodb_url}")

try:
    print(" Attempting to connect...")
    client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
    
    server_info = client.server_info()
    print(f" Connected to MongoDB successfully!")
    print(f" MongoDB Version: {server_info.get('version', 'Unknown')}\n")
    
    db = client["vibella_db"]
    collection = db["conversations"]
    print(f" Using Database: vibella_db")
    print(f" Using Collection: conversations\n")
    

    print("Inserting test document...")
    test_doc = {
        "user_message": "Hello Vibella!",
        "ai_response": "Hi! I'm ready to help with your Instagram content!",
        "timestamp": datetime.utcnow(),
        "test": True
    }
    
    result = collection.insert_one(test_doc)
    print(f"Test document inserted!")
    print(f"   Document ID: {result.inserted_id}\n")

    print("Retrieving test document...")
    found = collection.find_one({"_id": result.inserted_id})
    if found:
        print(f"Document retrieved successfully!")
        print(f"User Message: {found['user_message']}")
        print(f"AI Response: {found['ai_response']}\n")

    total_count = collection.count_documents({})
    print(f"Total documents in collection: {total_count}\n")
    
    print("Cleaning up test document...")
    collection.delete_one({"_id": result.inserted_id})
    print("Test document removed\n")
    
    print("="*60)
    print("SUCCESS! MongoDB is working perfectly!")
    print("="*60)
    print("Next steps:")
    print("   1. Run: python main.py")
    print("   2. Open frontend/index.html in your browser")
    print("   3. Start chatting with Vibella!\n")
    
except Exception as e:
    print("ERROR: Failed to connect to MongoDB\n")
    print(f"Error details: {e}\n")
    print("="*60)
    print("TROUBLESHOOTING STEPS:")
    print("="*60)
    print("1. Check if MongoDB service is running:")
    print("   - Press Win+R, type 'services.msc', press Enter")
    print("   - Look for 'MongoDB Server' and ensure it's 'Running'")
    print("   - If not, right-click and select 'Start'\n")
    
    print("2. Start MongoDB manually:")
    print("   - Open Command Prompt as Administrator")
    print("   - Run: net start MongoDB\n")
    
    print("3. Check MongoDB installation:")
    print("   - Default install path: C:\\Program Files\\MongoDB\\Server\\")
    print("   - Check if mongod.exe exists\n")
    
    print("4. Try restarting MongoDB service:")
    print("   - net stop MongoDB")
    print("   - net start MongoDB\n")
    
    print("5. Check MongoDB logs:")
    print("   - Usually at: C:\\Program Files\\MongoDB\\Server\\<version>\\log\\")
    
finally:
    if 'client' in locals():
        client.close()
        print("🔌 Connection closed")