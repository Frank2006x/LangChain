import os
import sys

from dotenv import load_dotenv
import google.generativeai as genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import  LLMChain


def load_api_key()->str:
    load_dotenv()
    key=os.getenv("GOOGLE_API_KEY")
    if not key:
        print("Key no found in env")
        sys.exit()
    return key

def pet_name(animal_type):
    try:
        api_key=load_api_key()
        genai.configure(api_key=api_key)
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.7)
        prompt_template_name=PromptTemplate(
            input_variables=["animal_type"],
            template="I have a {animal_type} pet.I want a cool name.I suggest me 5 cool name for my pet.note filler just return 5 names"
        )
        """Old way"""
        # name_chain=LLMChain(llm=llm,prompt=prompt_template_name)
        # print(name_chain)
        
        """New Way"""
        name_chain=prompt_template_name | llm
        
        res=name_chain.invoke({"animal_type":animal_type})
        return res.content

    
    except Exception as e:
        print(f"Error while generation{e}")
        return None
    
    
if __name__ =="__main__":
    print(pet_name("duck"))

