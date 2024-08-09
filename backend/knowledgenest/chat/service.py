import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
MODEL = "gpt-4o-mini"

def send_llm_message(message: str) -> str:
    """Simple llm invocation of OPENAI llm"""

    llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)
    chain = llm | StrOutputParser() 
    resp = chain.invoke(message)
    return resp


