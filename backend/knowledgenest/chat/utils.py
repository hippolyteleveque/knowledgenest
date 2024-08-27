import functools
from operator import itemgetter
from typing import Dict, List

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStore
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.runnables import chain

from knowledgenest.vector_database import get_vector_db
from knowledgenest.lib import (
    MISTRAL_LLM_MODEL,
    MISTRAL_EMBEDDING_MODEL,
    MISTRALAI_API_KEY,
)

SYSTEM_PROMPT = """You are a useful assistant that answers politey to users questions. 
            Your answers are based on your general knowledge but 
            you primarily based on the below context when it is useful :\n\n{context}"""


def create_retriever(vectorstore: VectorStore, filter: Dict) -> Runnable:

    def retrieve_documents(query: str, vectorstore, filter) -> List[Document]:
        docs, scores = zip(
            *vectorstore.similarity_search_with_score(query, k=3, filter=filter)
        )
        for doc, score in zip(docs, scores):
            doc.metadata["score"] = score

        return list(docs)

    retriever = functools.partial(
        retrieve_documents, vectorstore=vectorstore, filter=filter
    )

    @chain
    def retrieve(query: str) -> List[Document]:
        return retriever(query)

    return retrieve


def get_chain(user_id: str):
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
    retriever = create_retriever(vector_store, dict(user_id=user_id))
    chain = (
        dict(docs=parse_retriever_input | retriever, messages=itemgetter("messages"))
        | RunnableParallel(
            context=itemgetter("docs") | RunnableLambda(format_docs),
            messages=itemgetter("messages"),
            sources=itemgetter("docs") | RunnableLambda(parse_sources),
        )
        | RunnableParallel(
            prompt=prompt,
            sources=itemgetter("sources"),
        )
        | RunnableParallel(
            output=itemgetter("prompt") | llm | StrOutputParser(),
            sources=itemgetter("sources"),
        )
    )
    return chain


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


def parse_sources(docs: List[Document]) -> List[Dict]:
    """Extract unique sources with useful information"""
    sources = {}
    for doc in docs:
        doc_id = doc.metadata["content_id"]
        if doc_id not in sources:
            sources[doc_id] = {
                "id": doc_id,
                "type": doc.metadata["type"],
                "score": doc.metadata["score"],
            }

        elif sources[doc_id]["score"] < doc.metadata["score"]:
            # We take the best score of each document
            sources[doc_id]["score"] = doc.metadata["score"]
    return list(sources.values())
