import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print(" ERROR: GOOGLE_API_KEY not found in .env file")
    exit(1)

print(" API key found!")
print(f"Key starts with: {api_key[:10]}...")

try:
    print("\n Testing Gemini 2.5 Flash connection...")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key,
        convert_system_message_to_human=True
    )

    response = llm.invoke("Say 'Vibella is ready!' if you can hear me")
    
    print(" SUCCESS! Gemini responded:")
    print(f"   {response.content}")
    print("\n Your setup is working perfectly!")
    
except Exception as e:
    print(f" ERROR: {str(e)}")
    print("\nTroubleshooting tips:")
    print("1. Check your API key is correct")
    print("2. Make sure you have internet connection")
    print("3. Verify the API key is enabled in Google AI Studio")