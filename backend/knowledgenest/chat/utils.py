from typing import Dict, List, Optional

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import VectorStore
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.runnables import chain
from pinecone import Index

from knowledgenest.vector_database import get_vector_db
from knowledgenest.config import config

MISTRAL_LLM_MODEL = config.MISTRAL_LLM_MODEL
MISTRAL_EMBEDDING_MODEL = config.MISTRAL_EMBEDDING_MODEL
OPENAI_LLM_MODEL = config.OPENAI_LLM_MODEL
ANTHROPIC_LLM_MODEL = config.ANTHROPIC_LLM_MODEL

SYSTEM_PROMPT = """You are a useful assistant that answers politey to users questions. 
            Your answers are based on your general knowledge but 
            you primarily based on the below context when it is useful :\n\n{context}"""


class KNRag:

    def __init__(
        self,
        provider: str,
        filter: Optional[Dict[str, str]] = None,
        pc_idx: Optional[Index] = None,
    ):
        self._filter = filter
        self._provider = provider
        self._pc_idx = pc_idx
        self._retriever = self._init_retriever()
        self._llm = self._init_llm()

    def answer(self, params: dict, stream=True):
        docs = self._retriever.invoke(params)
        sources = self._parse_sources(docs)
        formatted_docs = self._format_docs(docs)
        if stream:
            output = self._llm.astream(dict(**params, context=formatted_docs))
        else:
            output = self._llm.invoke(dict(**params, context=formatted_docs))
        return {"sources": sources, "output": output}

    def _init_retriever(self):
        if self._pc_idx is None:
            self._pc_idx = get_vector_db()
        embeddings = MistralAIEmbeddings(model="mistral-embed")
        vector_store = PineconeVectorStore(index=self._pc_idx, embedding=embeddings)
        retriever = self._create_retriever(vector_store, self._filter)

        retriever_chain = self._parse_retriever_input | retriever
        return retriever_chain

    def _init_llm(self):
        llm = self._get_llm(self._provider)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        llm_chain = prompt | llm | StrOutputParser()
        return llm_chain

    def _format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def _parse_retriever_input(self, params: Dict):
        return params["messages"][-1].content

    def _parse_sources(self, docs: List[Document]) -> List[Dict]:
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

    def _create_retriever(
        self, vectorstore: VectorStore, filter: Dict | None
    ) -> Runnable:
        """Create and returns a retriever with the specified filters"""

        @chain
        def retrieve(query: str) -> List[Document]:
            if results := vectorstore.similarity_search_with_score(
                query, k=3, filter=filter
            ):
                docs, scores = zip(*results)
                for doc, score in zip(docs, scores):
                    doc.metadata["score"] = score

                return list(docs)
            return []

        return retrieve

    def _get_llm(self, ai_provider: str) -> Runnable:
        """Returns the langchain runnable llm based on the config"""
        if ai_provider == "mistral":
            return ChatMistralAI(model_name=MISTRAL_LLM_MODEL)
        elif ai_provider == "anthropic":
            return ChatAnthropic(model=ANTHROPIC_LLM_MODEL)
        elif ai_provider == "openai":
            return ChatOpenAI(model=OPENAI_LLM_MODEL)
        else:
            raise ValueError("Unknown provider {ai_provider}")
