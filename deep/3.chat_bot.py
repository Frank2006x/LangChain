import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

load_dotenv()


api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables")
    exit(1)


llm=ChatGoogleGenerativeAI(
     model="gemini-1.5-flash",
    google_api_key=api_key  
)

chatHistory=[]

SystemMessage=SystemMessage("You are friendly and helpfull assitant.Your name is Ajay")
chatHistory.append(SystemMessage)
while True:
    query=input("You : ")
    if query.lower()=="exit":
        break
    chatHistory.append(HumanMessage(content=query))
    res=llm.invoke(chatHistory)
    response=res.content
    chatHistory.append(AIMessage(content=response))
    
    print(f"AI : {response}")
    

    
    
    