import os
import sys

from dotenv import load_dotenv
import google.generativeai as genai

from  langchain_google_genai import ChatGoogleGenerativeAI


def load_api_key()->str:
    load_dotenv()
    key=os.getenv("GOOGLE_API_KEY")
    if not key:
        print("key not found in env")
        sys.exit()
    return key


      
def generate_pet_name():
    try:
        api_key=load_api_key()
        genai.configure(api_key=api_key)
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.7)
        name=llm.invoke("I have a dog pet .I need a cool name for it.list five names")
        return name.content
    except Exception as e:
        print(f"Error generating pet name: {e}")
        return None
    

if __name__=="__main__":
    res=generate_pet_name()
    if res:
        print(res)
