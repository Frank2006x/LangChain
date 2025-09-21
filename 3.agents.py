import os
import sys

from dotenv import load_dotenv
import google.generativeai as genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import wikipedia
import math

def load_api_key()->str:
    load_dotenv()
    key=os.getenv("GOOGLE_API_KEY")
    if not key:
        print("Key not found in env")
        sys.exit()
    return key

def wikipedia_search(query: str) -> str:
    """Search Wikipedia for information."""
    try:
        return wikipedia.summary(query, sentences=2)
    except:
        return "No information found on Wikipedia."

def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        # Simple calculator for basic operations
        result = eval(expression)
        return str(result)
    except:
        return "Invalid mathematical expression."

def langchainAgent():
    try:
        api_key=load_api_key()
        genai.configure(api_key=api_key)
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.7)
        
        # Create custom tools
        tools = [
            Tool(
                name="Wikipedia",
                func=wikipedia_search,
                description="Search Wikipedia for factual information about any topic."
            ),
            Tool(
                name="Calculator",
                func=calculator,
                description="Calculate mathematical expressions. Input should be a valid mathematical expression."
            )
        ]
        
        # Get the prompt template
        prompt = hub.pull("hwchase17/react")
        
        # Create agent
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        # Fixed question with better clarity
        res = agent_executor.invoke({
            "input": "area of circle with radius 3"
        })
        
        return res["output"]
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    result = langchainAgent()
    if result:
        print("\nFinal Answer:")
        print(result)
