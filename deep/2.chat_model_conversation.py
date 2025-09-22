import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables")
    exit(1)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key  
)

message=[
    SystemMessage("Consider you are an expert Minecraft player"),
    HumanMessage("Guide me to beat enderdragon")
]

try:
    res=llm.invoke(message)
    print(res.content)
except Exception as e:
    print(f"Error calling the API: {e}")