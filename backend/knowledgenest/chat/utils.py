from operator import itemgetter
from typing import Dict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from knowledgenest.vector_database import get_vector_db
from knowledgenest.lib import (
    MISTRAL_LLM_MODEL,
    MISTRAL_EMBEDDING_MODEL,
    MISTRALAI_API_KEY,
)

SYSTEM_PROMPT = """You are a useful assistant that answers politey to users questions. 
            Your answers are based on your general knowledge but 
            you primarily based on the below context when it is useful :\n\n{context}"""


def get_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    index = get_vector_db()
    llm = ChatMistralAI(model_name=MISTRAL_LLM_MODEL, api_key=MISTRALAI_API_KEY)
    embeddings = MistralAIEmbeddings(
        model=MISTRAL_EMBEDDING_MODEL, api_key=MISTRALAI_API_KEY
    )
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs=dict(k=3))
    chain = (
        dict(
            context=parse_retriever_input | retriever | format_docs,
            messages=itemgetter("messages"),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content
