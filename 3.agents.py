import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.agents import load_tools


def load_api_key() -> str:
    load_dotenv()
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("Key not found in env")
        sys.exit()
    return key


def langchainAgent():
    try:
        api_key = load_api_key()
        genai.configure(api_key=api_key)

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

        tools = load_tools(["wikipedia", "llm-math"], llm=llm)

        
        prompt = hub.pull("hwchase17/react")

        
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        
        res = agent_executor.invoke({
            "input": "number of people died last year by road accident"
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
